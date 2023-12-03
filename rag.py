# テキストデータベースの準備
from trafilatura import fetch_url, extract
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import configparser
import glob
import os

# 環境ファイル読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
# 文章分割設定
chunk_size = int(config_ini['RAG']['CHUNK_SIZE'])
chunk_overlap=int(config_ini['RAG']['CHUNK_OBERLAP'])
# 出力データ数
k_output=int(config_ini['RAG']['K_OUTPUT'])
# DBパス
db_path=config_ini['RAG']['DB_PATH']

# WEBページ内容取得
def get_webpage(root_path, urllist_path):
    try:
        # 過去のWEBページ本文削除
        file_list = glob.glob(root_path +"webpage*.txt")
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

# データベース更新
def update_database(root_path, model_name):
    try:
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
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        splitted_texts = text_splitter.split_documents(docs)
        
        # 文章からベクトルに変換するためのモデルを用意
        embeddings = HuggingFaceEmbeddings(model_name = model_name)
        # 文章データベースからベクトルデータベースを作成。チャンク単位で文章からベクトルに変換。
        global db
        db = FAISS.from_documents(splitted_texts, embeddings)
        db.save_local(db_path)

    except Exception as e:
        return "DB更新に失敗しました。詳細：" + str(e)

# 作成済データベースロード
def read_db(model_name):
    try:
        global db
        embeddings = HuggingFaceEmbeddings(model_name = model_name)
        db = FAISS.load_local(db_path, embeddings)
        return "DBの読み込みが成功しました。"
    
    except Exception as e:
        return "DBの読み込みが失敗しました。詳細：" + str(e)
    
def create_prompt(question):
    try:
        global db
        docs = db.similarity_search(question, k=k_output)
        ref_text = ''
        for i in range(len(docs)):
            ref_text += docs[i].page_content +'\n'
        prompt = PromptTemplate.from_template(
            '{question} ：\n 次の情報を参考に回答を作成してください。\n\n {ref_text}'
        )

        return prompt.format(question=question,ref_text=ref_text)
    
    except Exception as e:
        return "プロンプト生成に失敗しました。詳細：" + str(e)

if __name__ == '__main__':
    #print(read_db(config_ini['DEFAULT']['MODEL_NAME']))
    #print(create_prompt("質問に回答してください"))
    update_database(config_ini['DEFAULT']['LOAD_DATA_PATH'],config_ini['DEFAULT']['MODEL_NAME'])