import re
import os
import math
from collections import defaultdict

class SentimentAnalyzer:
    def __init__(self, data_dir="utilities/sentiment_data"):
        self.data_dir = data_dir
        self.positive_words = set()
        self.negative_words = set()
        self.neutral_words = set()
        self.intensifiers = set()
        self.negations = set()
        self.load_datasets()
    
    #Load all sentiment data and intensifiers    
    def load_datasets(self):
        try:
            self.load_sentiment_words()
            self.load_modifiers()
        except Exception as e:
            self.load_fallback_words()
    
    def load_sentiment_words(self):
        txt_files = {
            'positive': 'positive_words.txt',
            'negative': 'negative_words.txt',
            'neutral': 'neutral_words.txt'
        }
        
        for sentiment, filename in txt_files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    words = set(line.strip().lower() for line in f if line.strip())
                    setattr(self, f"{sentiment}_words", words)
            else:
                raise FileNotFoundError(f"Sentiment files {filename} not found")
            
            
    def load_modifiers(self):
        modifier_files = {
            'intensifiers': 'intensifiers.txt',
            'negations': 'negations.txt'
        }
        
        for modifier_type, filename in modifier_files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    words = set(line.strip().lower() for line in f if line.strip())
                    setattr(self, modifier_type, words)
            else:
                raise FileNotFoundError(f"Modifier file {filename} not found")
    
    
    def load_fallback_words(self):
        
        #Positive words
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic', 'wonderful',
            'perfect', 'perfectly', 'outstanding', 'brilliant', 'superb', 'terrific', 'marvelous',
            'love', 'like', 'enjoy', 'recommend', 'best', 'better', 'nice', 'satisfied',
            'happy', 'pleased', 'impressed', 'worth', 'valuable', 'effective', 'efficient',
            'reliable', 'durable', 'comfortable', 'easy', 'simple', 'fast', 'quick',
            'smooth', 'stable', 'clean', 'sharp', 'clear', 'bright', 'vibrant',
            'crisp', 'premium', 'quality', 'sturdy', 'solid', 'robust', 'strong',
            'powerful', 'efficient', 'responsive', 'speedy', 'instant', 'immediate',
            'seamless', 'flawless', 'optimal', 'superior', 'exceptional',
            'beautiful', 'elegant', 'stylish', 'sleek', 'modern', 'innovative',
            'intuitive', 'user-friendly', 'convenient', 'practical', 'functional',
            'versatile', 'flexible', 'adaptable', 'customizable',
            'affordable', 'reasonable', 'inexpensive', 'budget', 'worthwhile',
            'satisfying', 'pleasing', 'delightful', 'enjoyable', 'entertaining',
            'rewarding', 'gratifying', 'fulfilling',
            'helpful', 'supportive', 'friendly', 'professional', 'knowledgeable',
            'responsive', 'attentive', 'courteous', 'polite', 'respectful',
            'prompt', 'timely', 'accurate', 'precise', 'secure', 'safe', 'protected',
            'works', 'decent', 'impressive', 'performance', 'design', 'value', 'features', 'fine'
        }
        
        #Negative words
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'waste', 'disappointing',
            'poor', 'cheap', 'broken', 'damaged', 'defective', 'useless', 'worthless',
            'junk', 'garbage', 'trash', 'hate', 'dislike', 'regret', 'avoid',
            'problem', 'issue', 'error', 'fault', 'flaw', 'defect', 'bug', 'glitch',
            'failure', 'malfunction', 'breakdown', 'crash', 'freeze', 'hang',
            'slow', 'sluggish', 'laggy', 'unresponsive', 'delayed', 'frozen',
            'crashed', 'failed', 'malfunctioned', 'broke', 'shattered', 'cracked',
            'flimsy', 'fragile', 'brittle', 'weak', 'unstable', 'shaky',
            'wobbly', 'loose', 'tight', 'stiff', 'stuck', 'jammed', 'blocked',
            'uncomfortable', 'awkward', 'clumsy', 'bulky', 'heavy', 'light',
            'slippery', 'rough', 'sharp', 'dangerous', 'hazardous', 'risky',
            'rude', 'impolite', 'unhelpful', 'incompetent', 'ignorant',
            'unprofessional', 'disrespectful', 'arrogant', 'negligent',
            'late', 'delayed', 'lost', 'missing', 'crushed', 'bent', 'scratched',
            'dented', 'torn', 'ripped', 'stolen',
            'expensive', 'overpriced', 'costly', 'pricey', 'unaffordable',
            'waste', 'scam', 'fraud', 'fake', 'counterfeit', 'imitation',
            'angry', 'frustrated', 'annoyed', 'irritated', 'upset', 'disappointed',
            'sad', 'depressed', 'miserable', 'heartbroken', 'devastated',
            'complicated', 'confusing', 'difficult', 'hard', 'challenging',
            'frustrating', 'annoying', 'inconvenient', 'troublesome',
            'noisy', 'loud', 'quiet', 'silent', 'hot', 'cold', 'warm', 'cool',
            'dirty', 'dusty', 'grimy', 'stained', 'soiled', 'contaminated',
            'leaks', 'smells', 'burns', 'overheats', 'vibrates', 'shakes',
            'scratches', 'fades', 'peels', 'cracks', 'breaks', 'tears',
            'terrible', 'broken', 'unhelpful', 'nothing', 'not', 'good', 'bad', 
            'overheats', 'awful', 'hate', 'never', 'disappointing', 'expected'
        }
        
        #Neutral words
        self.neutral_words = {
            'okay', 'fine', 'average', 'mediocre', 'decent', 'adequate',
            'sufficient', 'acceptable', 'moderate', 'reasonable', 'standard',
            'small', 'large', 'big', 'little', 'much', 'many', 'few', 'several',
            'some', 'any', 'all', 'none', 'most', 'least',
            'basic', 'regular', 'normal', 'typical', 'usual', 'common',
            'ordinary', 'conventional', 'traditional',
            'process', 'method', 'system', 'approach', 'technique',
            'procedure', 'operation', 'function', 'feature',
            'product', 'item', 'support', 'quality', 'battery', 'life',
            'quickly', 'product', 'purchase', 'results', 'buying', 'again',
            'delivery', 'experience', 'arrived', 'special', 'could'
        }
        
        #Intensifiers
        self.intensifiers = {
            'very', 'really', 'extremely', 'absolutely', 'completely',
            'totally', 'utterly', 'highly', 'particularly', 'especially'
        }
        
        #Negations
        self.negations = {
            'not', "n't", 'no', 'never', 'none', 'nothing', 'without',
            'neither', 'nor', 'cannot', "can't", "won't", "wouldn't",
            "couldn't", "shouldn't", "isn't", "aren't", "wasn't", "weren't",
            "don't", "doesn't", "didn't", "haven't", "hasn't", "hadn't"
        }
        
    #Text Preprocessing
    def preprocess_text(self, text):
        if not text:
            return ""
        
        text = text.lower()
        text = re.sub(r'[^\w\s\']', ' ', text)
        text = re.sub(r"n't\b", " not", text)
        text = re.sub(r"'s\b", " is", text)
        text = re.sub(r"'re\b", " are", text)
        text = re.sub(r"'ll\b", " will", text)
        text = re.sub(r"'ve\b", " have", text)
        text = re.sub(r"'d\b", " would", text)
        text = re.sub(r"'m\b", " am", text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text):
        return re.findall(r'\b\w+\b', text)
    
    
    #Sentiment Analysis Algorithm
    def analyze_sentiment(self, text):
        
        processed_text = self.preprocess_text(text)
        tokens = self.tokenize(processed_text)
        
        positive_score = 0
        negative_score = 0
        intensity = 1.0
        negation_active = False
        
        found_positive = []
        found_negative = []
        found_neutral = []
        found_intensifiers = []
        found_negations = []
        
        for i, token in enumerate(tokens):
            word_info = {
                'word': token,
                'position': i,
                'negated': negation_active,
                'intensity': intensity
            }
            
            if token in self.intensifiers:
                intensity = 2.0
                found_intensifiers.append({
                    'word': token,
                    'position': i,
                    'multiplier': intensity
                })
                continue
            
            if token in self.negations:
                negation_active = True
                found_negations.append({
                    'word': token,
                    'position': i,
                    'active': True
                })
                continue
            
            if token in self.positive_words:
                score = intensity
                if negation_active:
                    score = -score
                    negative_score += abs(score)
                    word_info['contributed_score'] = -score
                    found_negative.append(word_info)
                else:
                    positive_score += score
                    word_info['contributed_score'] = score
                    found_positive.append(word_info)
                
                negation_active = False
                intensity = 1.0
            
            elif token in self.negative_words:
                score = intensity
                if negation_active:
                    score = -score
                    positive_score += abs(score)
                    word_info['contributed_score'] = abs(score)
                    found_positive.append(word_info)
                else:
                    negative_score += score
                    word_info['contributed_score'] = -score
                    found_negative.append(word_info)
                    
                negation_active = False
                intensity = 1.0
            
            elif token in self.neutral_words:
                word_info['contributed_score'] = 0
                found_neutral.append(word_info)
            
            else:
                negation_active = False
                intensity = 1.0
                
        total_sentiment_words = len(found_positive) + len(found_negative)
        
        if total_sentiment_words == 0:
            overall_sentiment = 'neutral'
            normalized_score = 0.0
        else:
            raw_score = positive_score - negative_score
            normalized_score = max(-1.0, min(1.0, raw_score/total_sentiment_words))
            
            if normalized_score > 0.1:
                overall_sentiment = 'positive'
            elif normalized_score < -0.1:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
        
        total_words = len(tokens)
        positive_percent = (len(found_positive) / total_words * 100) if total_words > 0 else 0
        negative_percent = (len(found_negative) / total_words * 100) if total_words > 0 else 0
        neutral_percent = (len(found_neutral) / total_words * 100) if total_words > 0 else 0
        
        detailed_analysis = {
            'sentiment': overall_sentiment,
            'score': round(normalized_score, 4),
            'percentages': {
                'positive': round(positive_percent, 2),
                'negative': round(negative_percent, 2),
                'neutral': round(neutral_percent, 2)
            },
            'word_counts': {
                'total': total_words,
                'positive': len(found_positive),
                'negative': len(found_negative),
                'neutral': len(found_neutral),
                'intensifiers': len(found_intensifiers),
                'negations': len(found_negations)
            },
            'word_details': {
                'positive_words': found_positive,
                'negative_words': found_negative,
                'neutral_words': found_neutral,
                'intensifiers': found_intensifiers,
                'negations': found_negations
            },
            'processed_text': processed_text
        }
        
        return overall_sentiment, round(normalized_score, 4), detailed_analysis
    

    #Summarization Algorithm
    def summarizer(self, text, sentences_per_section = 5):
        if not text or not text.strip():
            return {
                'positive': [],
                'negative': [],
                'neutral': []
            }
        sentences = self.split_into_sentences(text)
        if len(sentences) <= sentences_per_section * 3:
            return self.categorize(sentences)
        
        sentence_analysis = []
        for sentence in sentences:
            sentiment, score, details = self.analyze_sentiment(sentence)
            sentence_analysis.append({
                'sentence': sentence,
                'sentiment': sentiment,
                'score': score,
                'word_count': len(self.tokenize(self.preprocess_text(sentence))),
                'sentiment_strength': abs(score),
                'has_strong_words': (len(details['word_details']['positive_words']) > 0
                                     or len(details['word_details']['negative_words']) > 0)
            })
        
        positive_sentences = [s for s in sentence_analysis if s['sentiment'] == 'positive']
        negative_sentences = [s for s in sentence_analysis if s['sentiment'] == 'negative']
        neutral_sentences = [s for s in sentence_analysis if s['sentiment'] == 'neutral']
        
        summary = {
            'positive': self.select_representative(positive_sentences, sentences_per_section),
            'negative': self.select_representative(negative_sentences, sentences_per_section),
            'neutral': self.select_representative(neutral_sentences, sentences_per_section)
        }
        
        return summary
    
    def select_representative(self, sentences, max_sentences):
        if not sentences:
            return []
        
        if len(sentences) <= max_sentences:
            return [s['sentence'] for s in sentences]
        
        scored_sentences = []
        
        for s in sentences:
            sentiment_score = s['sentiment_strength'] * 0.5
            length_score = 0.0
            if 8 <= s['word_count'] <= 25:
                length_score = 0.3
            elif 5 <= s['word_count'] <= 30:
                length_score = 0.2
            else: 
                length_score = 0.1
                
            strong_words_score = 0.2 if s['has_strong_words'] else 0.0
            
            total_score = sentiment_score + length_score + strong_words_score
            scored_sentences.append((s, total_score))
        
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        selected = [s[0]['sentence'] for s in scored_sentences[:max_sentences]]
        
        return selected
    
    def categorize(self, sentences):
        summary = {'positive': [], 'negative': [], 'neutral': []}
        
        for sentence in sentences:
            sentiment, score, _ = self.analyze_sentiment(sentence)
            summary[sentiment].append(sentence)
    
        return summary
    
    def split_into_sentences(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            if char in '.!?':
                current_sentence = current_sentence.strip()
                if len(current_sentence) > 10:
                    current_sentence = re.sub(r'^[,\-\s]+', '', current_sentence)
                    if current_sentence:
                        sentences.append(current_sentence)
                current_sentence = ""
        
        if current_sentence.strip() and len(current_sentence.strip()) > 10:
            sentences.append(current_sentence.strip())
        
        return sentences
    
    def comprehensive_analysis(self, text):
        sentiment, score, details = self.analyze_sentiment(text)
        sentiment_summary = self.summarizer(text, sentences_per_section=3)
        

        total_sentences = sum(len(sentences) for sentences in sentiment_summary.values())
        
        sentiment_distribution = {
            'positive': len(sentiment_summary['positive']),
            'negative': len(sentiment_summary['negative']),
            'neutral': len(sentiment_summary['neutral']),
            'total': total_sentences
        }
           
        comprehensive_analysis = {
            'overview': {
                'sentiment': sentiment,
                'score': score,
                'sentiment_distribution': sentiment_distribution
            },
            'summary_by_sentiment': sentiment_summary,
            'detailed_metrics': {
                'percentages': details['percentages'],
                'word_counts': details['word_counts'],
                'total_words': details['word_counts']['total']
            },
            'word_analysis': details['word_details']
        }
        
        return comprehensive_analysis
    
