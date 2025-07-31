const loading = document.getElementById('loading');
const list = document.getElementById('product-list');
const errorMessage = document.getElementById('error-message');

loading.style.display = 'block';

fetch('/api/products')
  .then(response => {
    if (!response.ok) {
      throw new Error('Server error while fetching products.');
    }
    return response.json();
  })
  .then(products => {
    loading.style.display = 'none';

    if (!products.length) {
      list.innerHTML = "<li>No products available.</li>";
      return;
    }

    products.forEach(product => {
      const item = document.createElement('li');
      item.innerHTML = `
        <div class="product-name">${product.product_name}</div>
        <div class="product-price">₹${parseFloat(product.retail_price).toFixed(2)}</div>
      `;
      list.appendChild(item);
    });
  })
  .catch(err => {
    loading.style.display = 'none';
    errorMessage.innerText = err.message || 'Failed to load products.';
    console.error(err);
  });
