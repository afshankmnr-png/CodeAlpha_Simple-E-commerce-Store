
let cartCount = 0;
let cartItems = [];

function addToCart(productName, price) {
    cartCount++;

    cartItems.push({
        name: productName,
        price: price
    });

    document.getElementById("count").textContent = cartCount;

    alert(productName + " added to your cart!");
}

function showCart() {
    if (cartItems.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    let message = "Your Shopping Cart:\n\n";
    let total = 0;

    cartItems.forEach(function(item, index) {
        message += (index + 1) + ". " + item.name +
                   " - ₹" + item.price + "\n";
        total += item.price;
    });

    message += "\nTotal: ₹" + total;
    alert(message);
}

function clearCart() {
    cartCount = 0;
    cartItems = [];

    document.getElementById("count").textContent = cartCount;

    alert("Your cart has been cleared!");
}
