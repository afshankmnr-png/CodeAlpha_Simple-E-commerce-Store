
let cartItems = JSON.parse(localStorage.getItem("cartItems") || "[]");

function saveCart() {
    localStorage.setItem("cartItems", JSON.stringify(cartItems));
}

function addToCart(productName, price) {
    const existing = cartItems.find(item => item.name === productName);

    if (existing) {
        existing.quantity++;
    } else {
        cartItems.push({
            name: productName,
            price: price,
            quantity: 1
        });
    }

    saveCart();
    updateCartCount();
    alert(productName + " added to cart!");
}

function updateCartCount() {
    const count = document.getElementById("count");

    if (count) {
        count.textContent = cartItems.reduce(
            (sum, item) => sum + item.quantity, 0
        );
    }
}

function showCart() {
    window.location.href = "cart.html";
}

function displayCart() {
    const container = document.getElementById("cart-items");
    const totalElement = document.getElementById("cart-total");

    if (!container || !totalElement) return;

    container.innerHTML = "";
    let total = 0;

    if (cartItems.length === 0) {
        container.textContent = "Your cart is empty.";
        totalElement.textContent = "Total: ₹0";
        return;
    }

    cartItems.forEach((item, index) => {
        total += item.price * item.quantity;

        const row = document.createElement("div");
        row.style.padding = "10px";
        row.style.borderBottom = "1px solid #ddd";

        const name = document.createElement("p");
        name.textContent = item.name + " - ₹" + item.price;

        const quantity = document.createElement("p");
        quantity.textContent = "Quantity: " + item.quantity;

        const removeButton = document.createElement("button");
        removeButton.textContent = "Remove";
        removeButton.addEventListener("click", () => {
            cartItems.splice(index, 1);
            saveCart();
            displayCart();
            updateCartCount();
        });

        row.append(name, quantity, removeButton);
        container.appendChild(row);
    });

    totalElement.textContent = "Total: ₹" + total;
}

function clearCart() {
    cartItems = [];
    saveCart();
    displayCart();
    updateCartCount();
}

function checkout() {
    if (cartItems.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    alert("Cart ready! Online order processing will be added with the backend.");
}

document.addEventListener("DOMContentLoaded", () => {
    updateCartCount();
    displayCart();
});


