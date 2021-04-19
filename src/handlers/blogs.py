from src.config import db


class BlogManager:
    def __init__(self):
        self.db = db
        self.collction = "blog"
        
    def create_article(self, model):
        doc = db.collection(self.collction).document(str(model.slug)).get()
        if doc.exists:
            print("Duplicate Key Found. {}".format(doc.get('slug')))
            return False
        
        doc = self.db.collection(self.collction).document(str(model.slug)).set(model.dict())
        if not doc:
            raise("document not saved")
        return True
    
    def get_article(self, document):
        doc = db.collection(self.collction).document(document).get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise("No Details Found")
    
    def update_article(self, document, model):
        doc_ref = db.collection(self.collction).document(document).update(model.dict())
        if not doc_ref:
            raise("document not saved")
        return True
    
    def delete_article(self, document):
        doc_ref = db.collection(self.collction).document(document).delete()
        return True
    
    def get_all_articles(self):
        docs = db.collection(self.collction).stream()
        users_list = [doc.to_dict() for doc in docs ]
        return users_list
