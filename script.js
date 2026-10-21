
let cartCount = 0;

function addToCart() {
    cartCount++;

    document.getElementById("count").textContent =
        cartCount;

    alert("Product added to cart!");
}
