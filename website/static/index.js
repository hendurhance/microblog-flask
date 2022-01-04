
function like(postId) {
  // Get variables
  const likeCount = document.getElementById(`likes-count-${postId}`);
  const likeButton = document.getElementById(`like-button-${postId}`);


    fetch(`/like-post/${postId}`, { method: "POST" }) 
    .then((res) => res.json())
    .then((data) => {
      // Update like count
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) { // If user liked the post
        likeButton.className = "fas fa-thumbs-up";
      } else {
        // If user unliked the post
        likeButton.className = "far fa-thumbs-up";
      }
    })
    // Catch errors
    .catch((e) => alert("Could not like post."));
}
