document.addEventListener("DOMContentLoaded", () => {

    // Add to Cart Buttons
    document.querySelectorAll(".add-to-cart-btn").forEach(button => {
        button.addEventListener("click", async function() {
            let variantId = this.getAttribute("data-variant-id");
            let parentDiv = this.closest(".cart-buttons"); 
            let quantityContainer = parentDiv.querySelector(".d-flex"); 
            try {
                if (!variantId) throw new Error("Variant ID not found!");

                let response = await fetch(`http://localhost/proxy-api/add-to-cart/?action=add&variant_id=${variantId}`);  
                if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

                let data = await response.json();
                parentDiv.querySelector(".num").innerText = data.quantity;
            } catch (error) {
                console.error("Fetch Error:", error);
                alert("Something went wrong. Please try again later.");
            }
            this.classList.add("d-none"); 
            quantityContainer.classList.remove("d-none");
        });
    });

    // Increment Buttons
    document.querySelectorAll(".inc-btn").forEach(button => {
        button.addEventListener("click", async function() {
            try {
                let variantId = this.getAttribute("data-variant-id");
                if (!variantId) throw new Error("Variant ID not found!");

                let response = await fetch(`http://localhost/proxy-api/add-to-cart/?action=add&variant_id=${variantId}`);  
                if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

                let data = await response.json();
                this.closest(".cart-buttons").querySelector(".num").innerText = data.quantity;
            } catch (error) {
                console.error("Fetch Error:", error);
                alert("Something went wrong. Please try again later.");
            }
        });
    });

    // Decrement Buttons
    document.querySelectorAll(".dec-btn").forEach(button => {
        button.addEventListener("click", async function() {
            try {
                let variantId = this.getAttribute("data-variant-id"); 
                let parentDiv = this.closest(".cart-buttons");
                let quantityContainer = this.closest(".d-flex"); 
                let addToCartBtn = parentDiv.querySelector(".add-to-cart-btn"); 
                if (!variantId) throw new Error("Variant ID not found!");

                let response = await fetch(`http://localhost/proxy-api/add-to-cart/?action=remove&variant_id=${variantId}`);  
                if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

                let data = await response.json();
                parentDiv.querySelector(".num").innerText = data.quantity;
                if (data.quantity === 0) {
                    quantityContainer.classList.add("d-none");
                    addToCartBtn.classList.remove("d-none");
                }
            } catch (error) {
                console.error("Fetch Error:", error);
                alert("Something went wrong. Please try again later.");
            }
        });
    });

    // Cart Page Increment/Decrement Buttons
    document.querySelectorAll(".cart-inc-btn, .cart-dec-btn").forEach(button => {
        button.addEventListener("click", async function() {
            try {
                let variantId = this.getAttribute("data-variant-id"); 
                let quantityContainer = this.closest(".d-flex"); 
                let subtotalElement = document.querySelector("h4.text-end");
                let priceElement = document.querySelector(`td[variant-id="${variantId}"]`);
                if (!variantId) throw new Error("Variant ID not found!");

                let action = this.classList.contains("cart-inc-btn") ? "add" : "remove";
                let response = await fetch(`http://localhost/proxy-api/add-to-cart/?action=${action}&variant_id=${variantId}`);
                if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

                let data = await response.json();
                quantityContainer.querySelector(".num").innerText = data.quantity;

                if (action === "remove" && data.quantity === 0) {
                    this.closest("tr").remove();
                }

                subtotalElement.innerText = `Subtotal: ${data.subtotal}`;
                priceElement.innerText = `₹ ${data.total_amt}`;
            } catch (error) {
                console.error("Fetch Error:", error);
                alert("Something went wrong. Please try again later.");
            }
        });
    });

});
