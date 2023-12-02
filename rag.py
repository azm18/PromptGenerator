# テキストデータベースの準備
from trafilatura import fetch_url, extract
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import glob
import os

def get_webpage(root_path,urllist_path):
    try:
        # 過去のWEBページ本文削除
        file_list = glob.glob("webpage*.txt")
        for file in file_list:
            os.remove(file)
        
        # URLリストを取得
        url_list=[]
        with open(urllist_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                url_list.append(line.strip())

        # WEBページを読み込み
        for index, url in enumerate(url_list):
            filename = root_path + "webpage{}.txt".format(index)
            
            # WEBページ本文を取得
            http_response = fetch_url(url)
            html_content = extract(http_response)
            
            # WEBページ本文を保存
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
    except Exception as e:
        return "WEBページ取得に失敗しました。詳細：" + str(e)

def update_database(root_path,model_name):
    docs = []
    # txtファイルを読み込み
    for file in glob.glob(root_path+"/*.txt"):
        loader = TextLoader(file, encoding="utf-8")
        docs.extend(loader.load_and_split())

    # wordファイルを読み込み
    for file in glob.glob(root_path+"/*.docx"):
        loader= Docx2txtLoader(file)
        docs.extend(loader.load_and_split())

    # pdfファイルを読み込み
    for file in glob.glob(root_path+"/*.pdf"):
        loader= PyPDFLoader(file)
        docs.extend(loader.load_and_split())

    # 全文章を決まった長さの文章（チャンク）に分割して、文章データベースを作成
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=300,
        chunk_overlap=20,
    )
    splitted_texts = text_splitter.split_documents(docs)
    
    # 文章からベクトルに変換するためのモデルを用意
    embeddings = HuggingFaceEmbeddings(model_name = model_name)
    
    # 文章データベースからベクトルデータベースを作成。チャンク単位で文章からベクトルに変換。
    global db
    db = FAISS.from_documents(splitted_texts, embeddings)
    db.save_local("./vectorstore")

def read_db(model_name):
    global db
    try:
        embeddings = HuggingFaceEmbeddings(model_name = model_name)
        db = FAISS.load_local("./vectorstore", embeddings)

        return "DBの読み込み成功しました。"
    except Exception as e:
        return "DBの読み込み失敗しました。詳細：" + str(e)
    

def create_prompt(question):
    try:
        global db
        docs = db.similarity_search(question, k=10)
        prompt = question+"：\n 次の情報を参考に回答を作成してください。 \n"
        for i in range(len(docs)):
            prompt += docs[i].page_content +'\n'
        
        return prompt
    except Exception as e:
        return "プロンプト生成に失敗しました。詳細：" + str(e)

if __name__ == '__main__':
    path = "./load_data/"
    #updata_database(path)