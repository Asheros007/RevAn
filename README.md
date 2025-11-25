# RevAn: A Sentiment Analyzer and Summarizer
*A Django-based web application using HTML, CSS, Django, and PostgreSQL*

##Overview
This project is a web application that allows users to submit reviews either as text or as an uploaded file.
The system processes the input using a lexical-based sentiment analysis algorithm, generates a polarity score, and produces a summarized version of the review.

The goal is to offer a clean, efficient, and user-friendly way to analyze customer or user feedback at scale.

---
##Features
User Review Submission
  * Submit review as text
  * Upload review as a `.txt`
    
*  **Lexical-based Sentiment Analysis**

  * Calculates sentiment scores (Positive, Negative, Neutral)
  * Detects polarity based on modifiers
  * Detects intensity of any sentiment using intensifiers.
    
* **Review Summarization**

  * Provides a concise summary using a rule-based or extractive summarization method.
  * Extract positive, negative and neutral sentences based on the sentiment of words. It categorizes and display them.
    
* **Dashboard**
  * Displays sentiment results, summary output, and analytics
    
* **Database Integration**
  * PostgreSQL stores reviews, processed output, and timestamps
    
* **Responsive UI**
  * Frontend built with HTML & CSS
---

## Techs:

| Layer                 | Technology                                                |
| --------------------- | --------------------------------------------------------- |
| **Frontend**          | HTML, CSS                                                 |
| **Backend**           | Django (Python)                                           |
| **Database**          | PostgreSQL                                                |
| **Processing Engine** | Custom lexical sentiment algorithm + summarization module |

---

## How It Works

### **1. Input Collection**

Users can:

* Type a review in the text area
* Upload a file containing review text

### **2. Lexical Sentiment Algorithm**

The backend processes text by:

* Tokenizing words
* Matching tokens with a sentiment lexicon
* Applying weights and computing polarity
* Output: **Positive**, **Negative**, or **Neutral**

### **3. Summarization**

A rule-based/extractive summarizer:

* Selects key sentences based on sentiment of words in that sentence
* Categorize them into three category: positive, negative and neutral
* Select representative sentence and display a summary in three section: Positive, Area of Improvement and Additional Observations

---

## 📜 License

This project is licensed under the **MIT License**.

---

##  Author

**Arun Devkota**
For queries or suggestions, feel free to open an issue or contact.

---
