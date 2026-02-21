const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class Database {
  constructor() {
    this.dbPath = path.join(__dirname, '..', 'studybot.db');
    this.db = new sqlite3.Database(this.dbPath, (err) => {
      if (err) {
        console.error('Error opening database:', err.message);
      } else {
        console.log('Connected to SQLite database');
        this.initializeTables();
      }
    });
  }

  initializeTables() {
    // Create conversations table
    this.db.run(`
      CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Create messages table
    this.db.run(`
      CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
      )
    `);

    // Create topics table
    this.db.run(`
      CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        topic TEXT NOT NULL,
        message_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id),
        FOREIGN KEY (message_id) REFERENCES messages (id)
      )
    `);

    console.log('Database tables initialized');
  }

  // Conversation methods
  async createConversation(title = 'New Conversation') {
    return new Promise((resolve, reject) => {
      const sql = 'INSERT INTO conversations (title) VALUES (?)';
      this.db.run(sql, [title], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID, title, created_at: new Date().toISOString() });
        }
      });
    });
  }

  async getConversations() {
    return new Promise((resolve, reject) => {
      const sql = 'SELECT * FROM conversations ORDER BY updated_at DESC';
      this.db.all(sql, [], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  async getConversation(id) {
    return new Promise((resolve, reject) => {
      const sql = 'SELECT * FROM conversations WHERE id = ?';
      this.db.get(sql, [id], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row);
        }
      });
    });
  }

  // Message methods
  async addMessage(conversationId, role, content) {
    return new Promise((resolve, reject) => {
      const sql = 'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)';
      this.db.run(sql, [conversationId, role, content], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID, conversation_id: conversationId, role, content });
        }
      });
    });
  }

  async getMessages(conversationId) {
    return new Promise((resolve, reject) => {
      const sql = 'SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC';
      this.db.all(sql, [conversationId], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  // Topic methods
  async addTopic(conversationId, topic, messageId) {
    return new Promise((resolve, reject) => {
      const sql = 'INSERT INTO topics (conversation_id, topic, message_id) VALUES (?, ?, ?)';
      this.db.run(sql, [conversationId, topic, messageId], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID, conversation_id: conversationId, topic, message_id: messageId });
        }
      });
    });
  }

  async getTopics(conversationId) {
    return new Promise((resolve, reject) => {
      const sql = 'SELECT DISTINCT topic FROM topics WHERE conversation_id = ? ORDER BY created_at DESC';
      this.db.all(sql, [conversationId], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows.map(row => row.topic));
        }
      });
    });
  }

  // Update conversation timestamp
  async updateConversationTimestamp(conversationId) {
    return new Promise((resolve, reject) => {
      const sql = 'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?';
      this.db.run(sql, [conversationId], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.changes > 0);
        }
      });
    });
  }

  close() {
    this.db.close((err) => {
      if (err) {
        console.error('Error closing database:', err.message);
      } else {
        console.log('Database connection closed');
      }
    });
  }
}

module.exports = new Database();
