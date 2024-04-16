

## 起動手順

### 1. Anaconda仮想環境の作成とライブラリのインストール

./english_test/english ディレクトリ下で、以下コマンドを実行。
```
conda create -n word-learner-app python django pandas nltk
```

### 2. 仮想環境起動
```
conda activate word-learner-app 
```

### 3. アプリの起動

./english_test/english ディレクトリ下で、以下コマンドを実行。
ターミナルに表示されているURLにアクセスしてアプリを起動。
```
python manage.py runserver
```


## アプリの機能

### 1. 選択問題
英文と英単語が表示され、6択から意味を選ぶ。
回答したら、下に正答が表示される。

<img width="846" alt="スクリーンショット 2024-04-17 0 01 59" src="https://github.com/t-k1208/Word-Learner-App/assets/132872794/925086cf-62f1-47e3-b156-ae59fd30db21">

### 2. 穴埋め問題
英文の空欄に入る英単語を入力する。

「Send」ボタンまたはエンターキーを押すと、完全な英文と日文、左下に入力した単語とその正誤が表示される。
右下には正解の単語と意味が表示される。

正解すると出題されなくなり、全て正解するまで間違えた問題がランダムで出題される。
全て正解するとリセットされる。

<img width="846" alt="スクリーンショット 2024-04-17 0 05 11" src="https://github.com/t-k1208/Word-Learner-App/assets/132872794/b8efe242-0dcb-407c-ab68-0376d891f710">

### 3. 一覧・作成
英単語、意味、英文、日文を登録する。
動詞は現在形で登録する。英文中で単語が過去形や現在進行形であっても、形態素解析で単語を判定して穴埋め問題が作成される。

右上の「CSV出力」ボタンで　./english_test/english ディレクトリ下に、登録したデータと正解・不正解の回数の一覧がcsv形式で出力される。
また、「間違えた順に切り替え」ボタンで、不正解の回数が多い単語順に一覧を並べ替えられる。

<img width="975" alt="スクリーンショット 2024-04-17 0 12 21" src="https://github.com/t-k1208/Word-Learner-App/assets/132872794/d6a4acc6-accc-465c-b8e6-0c29937b4042">


### 4. 修正・削除
登録したデータの修正。

<img width="975" alt="スクリーンショット 2024-04-17 0 21 56" src="https://github.com/t-k1208/Word-Learner-App/assets/132872794/9901577d-c364-40f0-b428-04404b9d3856">

検索欄から文字列の部分一致で探すことができる。
ここからデータの削除も行える。

<img width="975" alt="スクリーンショット 2024-04-17 0 25 55" src="https://github.com/t-k1208/Word-Learner-App/assets/132872794/b2a7af74-9e9f-432d-aa4f-c6e5f888bdca">


### 5. 設定　（未実装）
