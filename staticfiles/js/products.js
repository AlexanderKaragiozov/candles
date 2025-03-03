document.addEventListener("DOMContentLoaded", function () {
    const productGrid = document.getElementById("productGrid");
    const sortSelect = document.getElementById("sortProducts");
    const categoryFilter = document.getElementById("categoryFilter");
    const priceFilter = document.getElementById("priceFilter");
    const priceValue = document.getElementById("priceValue");

    // Store all products at the beginning
    let allProducts = Array.from(document.querySelectorAll(".product-item")).map(product => ({
        element: product,
        category: product.getAttribute("data-category"),
        price: parseFloat(product.getAttribute("data-price"))
    }));

    function renderProducts(filteredProducts) {
        productGrid.innerHTML = "";
        filteredProducts.forEach(product => productGrid.appendChild(product.element));
    }

    function filterAndSortProducts() {
        let filteredProducts = allProducts.filter(product =>
            (categoryFilter.value === "all" || product.category === categoryFilter.value) &&
            (product.price <= parseFloat(priceFilter.value))
        );

        if (sortSelect.value === "low-high") {
            filteredProducts.sort((a, b) => a.price - b.price);
        } else if (sortSelect.value === "high-low") {
            filteredProducts.sort((a, b) => b.price - a.price);
        }

        renderProducts(filteredProducts);
    }

    sortSelect.addEventListener("change", filterAndSortProducts);
    categoryFilter.addEventListener("change", filterAndSortProducts);
    priceFilter.addEventListener("input", function () {
        priceValue.innerText = priceFilter.value;
        filterAndSortProducts();
    });

    // Initial Render
    filterAndSortProducts();
});
