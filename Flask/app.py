from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

# Flask 앱 생성 및 시크릿 키 설정 (플래시 메시지용)
app = Flask(__name__)
app.secret_key = 'crud_post_practice’'

# MySQL 데이터베이스 연결 정보
CRUD_DB = {
    'host': 'mysql',
    'user': 'halo',
    'password': '1234',
    'database': 'CRUDPOST',
    'charset': 'utf8mb4'
}

# DB 연결 함수
def db_connect():
    """MySQL 데이터베이스 연결을 반환하는 함수"""
    return pymysql.connect(**CRUD_DB)

# 메인 페이지 - 게시물 목록 표시
@app.route('/')
def index():
    """
    게시판 메인 페이지로 이동.
    CRUD_POST 테이블에서 모든 게시물을 작성 시간 기준으로 내림차순 정렬하여 표시.
    """
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM CRUD_POST ORDER BY Create_time DESC")
        posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# 게시글 생성
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """
    새 게시글을 작성.
    POST 요청 시 데이터베이스에 제목과 내용을 추가한 후 메인 페이지로 리다이렉트.
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = db_connect()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO CRUD_POST (POST_title, POST_contents) VALUES (%s, %s)",
                (title, content)
            )
            conn.commit()
        conn.close()
        flash('게시글 추가 완료')  # 플래시 메시지 표시
        return redirect(url_for('index'))
    return render_template('create_post.html')  # GET 요청 시 작성 페이지 표시

# 게시글 읽기
@app.route('/read/<int:post_id>')
def read_post(post_id):
    """
    특정 게시글 읽기.
    POST_id를 기반으로 데이터베이스에서 게시글 정보를 가져와 상세 페이지로 전달.
    """
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM CRUD_POST WHERE POST_id = %s", (post_id,))
        post = cursor.fetchone()
    conn.close()
    return render_template('read_post.html', post=post)

# 게시글 수정
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """
    특정 게시글 수정.
    POST 요청 시 제목과 내용을 수정하고 메인 페이지로 리다이렉트.
    GET 요청 시 수정 페이지 표시.
    """
    conn = db_connect()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE CRUD_POST SET POST_title = %s, POST_contents = %s WHERE POST_id = %s",
                (title, content, post_id)
            )
            conn.commit()
        conn.close()
        flash('게시글 수정 완료')  # 플래시 메시지 표시
        return redirect(url_for('index'))
    else:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM CRUD_POST WHERE POST_id = %s", (post_id,))
            post = cursor.fetchone()
        conn.close()
        return render_template('update_post.html', post=post)

# 게시글 삭제
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """
    게시글 삭제.
    POST_id를 기반으로 데이터베이스에서 해당 게시글을 삭제한 후 메인 페이지로 리다이렉트.
    """
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM CRUD_POST WHERE POST_id = %s", (post_id,))
        conn.commit()
    conn.close()
    flash('게시글 삭제 완료')  # 플래시 메시지 표시
    return redirect(url_for('index'))

# 게시글 검색
@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    게시글 검색.
    제목, 내용, 전체 내용을 검색할 수 있으며 검색 결과를 메인 페이지에 표시.
    """
    query = request.args.get('query')  # 검색어
    search_type = request.args.get('type', 'all')  # 검색 범위: 제목, 내용, 또는 전체

    conn = db_connect()
    with conn.cursor() as cursor:
        if search_type == 'title':
            cursor.execute("SELECT * FROM CRUD_POST WHERE POST_title LIKE CONCAT('%%', %s, '%%')", (query,))
        elif search_type == 'content':
            cursor.execute("SELECT * FROM CRUD_POST WHERE POST_contents LIKE CONCAT('%%', %s, '%%')", (query,))
        else:
            cursor.execute(
                "SELECT * FROM CRUD_POST WHERE POST_title LIKE CONCAT('%%', %s, '%%') OR POST_contents LIKE CONCAT('%%', %s, '%%')",
                (query, query)
            )
        results = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=results, query=query, search_type=search_type)

# 앱 실행
if __name__ == '__main__':
    """
    애플리케이션 실행.
    Flask 서버는 0.0.0.0 호스트에서 5000번 포트로 실행되며 디버그 모드 활성화.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)
