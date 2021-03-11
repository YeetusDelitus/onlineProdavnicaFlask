let searchBar = document.querySelector('#searchBar');
const searchBtn = document.querySelector('#searchBtn');
let posts = document.querySelectorAll('.card-title')
const fileInput = document.querySelector('#image')
let imageLabel = document.querySelector('#imageLabel')

function deletePost(postId){
    fetch('delete-post',{
        method: 'POST',
        body: JSON.stringify({ postId: postId })
    }).then((_res) =>{
        window.location.href = '/';
    })
}

function searchPosts(){
    if (searchBar.value !== ''){
        for (let index = 0; index < posts.length; index++) {
            let postName = posts[index].textContent;
            if (postName.toLowerCase() != searchBar.value.toLowerCase()){
                posts[index].parentNode.parentNode.style.visibility = 'hidden';
            }
        }
    } else{
        for (let index = 0; index < posts.length; index++) {
            posts[index].parentNode.parentNode.style.visibility = 'visible';
        }
    }
}

function deleteAccount(user){
    if(confirm('Are you sure you want to delete an Account?')){
    fetch('delete-account', {
        method: 'POST',
        body: JSON.stringify(user)
    })
    }
}

function reportPost(productId){
    if(confirm('Are you sure you want to report a post?')){
        fetch('report-post', {
            method: 'POST',
            body: JSON.stringify(productId)
        })
    }
}

fileInput.onchange = () => {
    const selectedFile = fileInput.files[0];
    imageLabel.placeholder = selectedFile.name;
    console.log(imageLabel);
}