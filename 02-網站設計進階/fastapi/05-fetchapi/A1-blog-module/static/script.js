const API_URL = "http://127.0.0.1:8000/articles";

// 讀取所有文章
async function fetchArticles() {
    const response = await fetch(API_URL);
    const articles = await response.json();
    const main = document.getElementById("main");
    main.innerHTML = `<p><a href="#createNewArticle" onclick="createNewArticle()">Create New Article</a></p>\n`;
    articles.forEach(article => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `<a href="#viewArticle/${article.id}" onclick="viewArticle(${article.id})">${article.title}</a>`;
        main.appendChild(listItem);
    });
}

// 顯示單篇文章
async function viewArticle(articleId) {
    const response = await fetch(`${API_URL}/${articleId}`);
    if (response.status === 404) {
        alert("Article not found");
        return;
    }
    const article = await response.json();
    const main = document.getElementById("main");
    main.innerHTML = `
        <h2>${article.title}</h2>
        <p>${article.content}</p>
    `;
}

async function createNewArticle() {
    const main = document.getElementById("main");
    main.innerHTML = `
    <h1>New Post</h1>
    <p>Create a new post.</p>
    <form id="create-article-form">
        <input type="text" name="title" id="title" placeholder="Title" required>
        <br>
        <textarea name="content" id="content" placeholder="Content" required></textarea>
        <br>
        <button type="submit">Submit</button>
    </form>`;
    document.getElementById("create-article-form").addEventListener("submit", submitArticle);
}

// 提交新文章
async function submitArticle(event) {
    event.preventDefault();
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content })
    });
    console.log('response=', response)
    if (response.status === 400) {
        alert("Title and content are required");
        return;
    }

    window.location.hash = '#'
}

/*
// 初始化頁面
document.addEventListener("DOMContentLoaded", () => {
    fetchArticles();
});
*/

window.onhashchange = async function () {
    var r
    var tokens = window.location.hash.split('/')
    console.log('tokens=', tokens)
    switch (tokens[0]) {
      case '#createNewArticle':
        createNewArticle()
        break
      case '#viewArticle':
        viewArticle(tokens[1])
        break
      default:
        fetchArticles()
        break
    }
  }
  
  window.onload = function () {
    window.onhashchange()
  }
  
