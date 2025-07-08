// Global Price Comparison Tool JavaScript 

const sampleData = {
  // boAt Airdopes 161 - Multiple countries
  "US_boAt": [
    {
      "link": "#",
      "price": "35.00",
      "currency": "USD",
      "productName": "boAt Airdopes 161 (Imported)",
      "vendor": "Third-party Importer",
      "availability": "limited_stock",
      "note": "Not officially available in US"
    },
    {
      "link": "#",
      "price": "42.00",
      "currency": "USD",
      "productName": "boAt Airdopes 161 TWS (Import)",
      "vendor": "eBay Seller",
      "availability": "limited_stock",
      "note": "International shipping required"
    }
  ],
  
  "IN_boAt": [
    {
      "link": "https://www.boat-lifestyle.com/products/airdopes-161",
      "price": "899.00",
      "currency": "INR",
      "productName": "boAt Airdopes 161 TWS Earbuds with 40H Playback",
      "vendor": "boAt Official Store",
      "availability": "in_stock"
    },
    {
      "link": "https://www.flipkart.com/boat-airdopes-161",
      "price": "999.00",
      "currency": "INR",
      "productName": "boAt Airdopes 161 True Wireless Earbuds",
      "vendor": "Flipkart",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.in/dp/boAtAirdopes161",
      "price": "1099.00",
      "currency": "INR",
      "productName": "boAt Airdopes 161 Wireless Earbuds",
      "vendor": "Amazon India",
      "availability": "in_stock"
    }
  ],

  "UK_boAt": [
    {
      "link": "#",
      "price": "28.00",
      "currency": "GBP",
      "productName": "boAt Airdopes 161 (Imported)",
      "vendor": "Import Specialist",
      "availability": "limited_stock",
      "note": "Not officially available in UK"
    }
  ],

  "JP_boAt": [
    {
      "link": "#",
      "price": "4500.00",
      "currency": "JPY",
      "productName": "boAt Airdopes 161 (輸入品)",
      "vendor": "Import Store",
      "availability": "limited_stock",
      "note": "Not officially available in Japan"
    }
  ],

  // iPhone 16 Pro - All countries
  "US_iPhone": [
    {
      "link": "https://www.apple.com/iphone-16-pro/",
      "price": "999.00",
      "currency": "USD",
      "productName": "Apple iPhone 16 Pro 128GB Natural Titanium",
      "vendor": "Apple Store",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.com/dp/iPhone16Pro",
      "price": "999.00",
      "currency": "USD",
      "productName": "iPhone 16 Pro (128GB) - Natural Titanium",
      "vendor": "Amazon",
      "availability": "in_stock"
    },
    {
      "link": "https://www.bestbuy.com/site/iphone-16-pro",
      "price": "999.00",
      "currency": "USD",
      "productName": "Apple iPhone 16 Pro 128GB Unlocked",
      "vendor": "Best Buy",
      "availability": "in_stock"
    }
  ],

  "IN_iPhone": [
    {
      "link": "https://www.apple.com/in/iphone-16-pro/",
      "price": "119900.00",
      "currency": "INR",
      "productName": "Apple iPhone 16 Pro 128GB Natural Titanium",
      "vendor": "Apple Store India",
      "availability": "in_stock"
    },
    {
      "link": "https://www.flipkart.com/apple-iphone-16-pro",
      "price": "119900.00",
      "currency": "INR",
      "productName": "Apple iPhone 16 Pro (128GB) Natural Titanium",
      "vendor": "Flipkart",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.in/dp/iPhone16Pro",
      "price": "119900.00",
      "currency": "INR",
      "productName": "iPhone 16 Pro 128GB Natural Titanium",
      "vendor": "Amazon India",
      "availability": "in_stock"
    }
  ],

  "UK_iPhone": [
    {
      "link": "https://www.apple.com/uk/iphone-16-pro/",
      "price": "999.00",
      "currency": "GBP",
      "productName": "Apple iPhone 16 Pro 128GB Natural Titanium",
      "vendor": "Apple Store UK",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.co.uk/dp/iPhone16Pro",
      "price": "999.00",
      "currency": "GBP",
      "productName": "iPhone 16 Pro (128GB) Natural Titanium",
      "vendor": "Amazon UK",
      "availability": "in_stock"
    },
    {
      "link": "https://www.currys.co.uk/iphone-16-pro",
      "price": "999.00",
      "currency": "GBP",
      "productName": "Apple iPhone 16 Pro 128GB Unlocked",
      "vendor": "Currys",
      "availability": "in_stock"
    }
  ],

  "JP_iPhone": [
    {
      "link": "https://www.apple.com/jp/iphone-16-pro/",
      "price": "159800.00",
      "currency": "JPY",
      "productName": "Apple iPhone 16 Pro 128GB ナチュラルチタニウム",
      "vendor": "Apple Store Japan",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.co.jp/dp/iPhone16Pro",
      "price": "159800.00",
      "currency": "JPY",
      "productName": "iPhone 16 Pro (128GB) ナチュラルチタニウム",
      "vendor": "Amazon Japan",
      "availability": "in_stock"
    },
    {
      "link": "https://www.yodobashi.com/iphone-16-pro",
      "price": "159800.00",
      "currency": "JPY",
      "productName": "Apple iPhone 16 Pro 128GB",
      "vendor": "Yodobashi Camera",
      "availability": "in_stock"
    }
  ],

  // Samsung Galaxy S24 - All countries
  "US_Samsung": [
    {
      "link": "https://www.samsung.com/us/smartphones/galaxy-s24/",
      "price": "699.99",
      "currency": "USD",
      "productName": "Samsung Galaxy S24 128GB Marble Gray",
      "vendor": "Samsung US",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.com/samsung-galaxy-s24",
      "price": "419.00",
      "currency": "USD",
      "productName": "Samsung Galaxy S24 128GB (Best Deal)",
      "vendor": "Amazon US",
      "availability": "in_stock"
    },
    {
      "link": "https://www.bestbuy.com/samsung-galaxy-s24",
      "price": "549.99",
      "currency": "USD",
      "productName": "Samsung Galaxy S24 128GB Unlocked",
      "vendor": "Best Buy",
      "availability": "in_stock"
    }
  ],

  "UK_Samsung": [
    {
      "link": "https://www.samsung.com/uk/smartphones/galaxy-s24/",
      "price": "450.00",
      "currency": "GBP",
      "productName": "Samsung Galaxy S24 128GB Onyx Black",
      "vendor": "Samsung UK",
      "availability": "in_stock"
    },
    {
      "link": "https://www.idealo.co.uk/samsung-galaxy-s24",
      "price": "398.90",
      "currency": "GBP",
      "productName": "Samsung Galaxy S24 128GB (Best Deal)",
      "vendor": "Idealo UK",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.co.uk/dp/SamsungS24",
      "price": "450.00",
      "currency": "GBP",
      "productName": "Samsung Galaxy S24 128GB Unlocked",
      "vendor": "Amazon UK",
      "availability": "in_stock"
    }
  ],

  "IN_Samsung": [
    {
      "link": "https://www.samsung.com/in/smartphones/galaxy-s24/",
      "price": "42900.00",
      "currency": "INR",
      "productName": "Samsung Galaxy S24 128GB Onyx Black",
      "vendor": "Samsung India",
      "availability": "in_stock"
    },
    {
      "link": "https://www.flipkart.com/samsung-galaxy-s24",
      "price": "44999.00",
      "currency": "INR",
      "productName": "Samsung Galaxy S24 128GB",
      "vendor": "Flipkart",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.in/samsung-galaxy-s24",
      "price": "43900.00",
      "currency": "INR",
      "productName": "Samsung Galaxy S24 128GB Marble Gray",
      "vendor": "Amazon India",
      "availability": "in_stock"
    }
  ],

  "JP_Samsung": [
    {
      "link": "https://www.samsung.com/jp/smartphones/galaxy-s24/",
      "price": "89800.00",
      "currency": "JPY",
      "productName": "Samsung Galaxy S24 128GB オニキスブラック",
      "vendor": "Samsung Japan",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.co.jp/samsung-galaxy-s24",
      "price": "92000.00",
      "currency": "JPY",
      "productName": "Samsung Galaxy S24 128GB",
      "vendor": "Amazon Japan",
      "availability": "in_stock"
    }
  ],

  // Nintendo Switch - All countries
  "US_Nintendo": [
    {
      "link": "https://www.nintendo.com/us/gaming-systems/switch/",
      "price": "299.99",
      "currency": "USD",
      "productName": "Nintendo Switch with Neon Blue and Neon Red Joy‑Con",
      "vendor": "Nintendo US",
      "availability": "in_stock"
    },
    {
      "link": "https://www.walmart.com/nintendo-switch",
      "price": "299.00",
      "currency": "USD",
      "productName": "Nintendo Switch w/ Neon Blue & Neon Red Joy-Con",
      "vendor": "Walmart",
      "availability": "in_stock"
    },
    {
      "link": "https://www.bestbuy.com/nintendo-switch",
      "price": "299.99",
      "currency": "USD",
      "productName": "Nintendo Switch Console with Gray Joy-Con",
      "vendor": "Best Buy",
      "availability": "in_stock"
    }
  ],

  "JP_Nintendo": [
    {
      "link": "https://www.nintendo.com/jp/hardware/switch/",
      "price": "29980.00",
      "currency": "JPY",
      "productName": "Nintendo Switch ネオンブルー・ネオンレッド",
      "vendor": "Nintendo Japan",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.co.jp/dp/NintendoSwitch",
      "price": "32978.00",
      "currency": "JPY",
      "productName": "Nintendo Switch 本体 グレー",
      "vendor": "Amazon Japan",
      "availability": "in_stock"
    },
    {
      "link": "https://www.yodobashi.com/nintendo-switch",
      "price": "29980.00",
      "currency": "JPY",
      "productName": "Nintendo Switch Joy-Con(L)/(R) グレー",
      "vendor": "Yodobashi Camera",
      "availability": "in_stock"
    }
  ],

  "UK_Nintendo": [
    {
      "link": "https://www.nintendo.co.uk/Nintendo-Switch/",
      "price": "279.99",
      "currency": "GBP",
      "productName": "Nintendo Switch with Neon Blue and Neon Red Joy-Con",
      "vendor": "Nintendo UK",
      "availability": "in_stock"
    },
    {
      "link": "https://www.amazon.co.uk/nintendo-switch",
      "price": "279.99",
      "currency": "GBP",
      "productName": "Nintendo Switch Console with Gray Joy-Con",
      "vendor": "Amazon UK",
      "availability": "in_stock"
    },
    {
      "link": "https://www.game.co.uk/nintendo-switch",
      "price": "279.99",
      "currency": "GBP",
      "productName": "Nintendo Switch Neon Console",
      "vendor": "GAME",
      "availability": "in_stock"
    }
  ],

  "IN_Nintendo": [
    {
      "link": "#",
      "price": "27500.00",
      "currency": "INR",
      "productName": "Nintendo Switch (Imported)",
      "vendor": "Local Importer",
      "availability": "limited_stock",
      "note": "Not officially available in India"
    },
    {
      "link": "#",
      "price": "29999.00",
      "currency": "INR",
      "productName": "Nintendo Switch Console (Import)",
      "vendor": "Gaming Store",
      "availability": "limited_stock",
      "note": "International warranty may not apply"
    }
  ]
};

// Countries data
const countries = [
  {"code": "US", "name": "United States", "currency": "USD", "flag": "🇺🇸"},
  {"code": "IN", "name": "India", "currency": "INR", "flag": "🇮🇳"},
  {"code": "UK", "name": "United Kingdom", "currency": "GBP", "flag": "🇬🇧"},
  {"code": "JP", "name": "Japan", "currency": "JPY", "flag": "🇯🇵"}
];

// DOM Elements
const searchForm = document.getElementById('searchForm');
const countrySelect = document.getElementById('country');
const queryInput = document.getElementById('query');
const searchBtn = document.getElementById('searchBtn');
const btnText = searchBtn.querySelector('.btn-text');
const btnSpinner = searchBtn.querySelector('.btn-spinner');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const resultsTitle = document.getElementById('resultsTitle');
const resultsCount = document.getElementById('resultsCount');
const resultsGrid = document.getElementById('resultsGrid');

// Example buttons
const exampleButtons = document.querySelectorAll('.example-btn');

// Current search state
let isSearching = false;

// Initialize the application
function init() {
  setupEventListeners();
  setupExampleButtons();
  addEnhancedAnimations();
}

// Set up event listeners
function setupEventListeners() {
  searchForm.addEventListener('submit', handleSearch);
  
  // Add focus animations to form elements
  const formControls = document.querySelectorAll('.form-control');
  formControls.forEach(control => {
    control.addEventListener('focus', handleFocusIn);
    control.addEventListener('blur', handleFocusOut);
  });
}

// Enhanced focus animations
function handleFocusIn(event) {
  event.target.style.transform = 'scale(1.02)';
  event.target.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
}

function handleFocusOut(event) {
  event.target.style.transform = 'scale(1)';
}

// Set up example buttons with enhanced animations
function setupExampleButtons() {
  exampleButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      // Add click animation
      button.style.transform = 'scale(0.95)';
      setTimeout(() => {
        button.style.transform = 'scale(1)';
      }, 150);
      
      const country = button.getAttribute('data-country');
      const query = button.getAttribute('data-query');
      
      // Set form values with animation
      countrySelect.value = country;
      queryInput.value = query;
      
      // Add highlight animation to form fields
      animateFormFields();
      
      // Trigger search
      handleSearch(new Event('submit'));
    });
  });
}

// Animate form fields when populated
function animateFormFields() {
  [countrySelect, queryInput].forEach((field, index) => {
    setTimeout(() => {
      field.style.background = 'rgba(102, 126, 234, 0.1)';
      field.style.borderColor = '#667eea';
      field.style.transform = 'scale(1.02)';
      
      setTimeout(() => {
        field.style.background = 'white';
        field.style.borderColor = 'rgba(0, 0, 0, 0.1)';
        field.style.transform = 'scale(1)';
      }, 1000);
    }, index * 200);
  });
}

// Add enhanced animations to existing elements
function addEnhancedAnimations() {
  // Add stagger animation to feature cards
  const featureCards = document.querySelectorAll('.feature-card');
  featureCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    
    setTimeout(() => {
      card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 200);
  });
  
  // Add hover animations to example buttons
  exampleButtons.forEach(button => {
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'translateY(-4px) scale(1.02)';
    });
    
    button.addEventListener('mouseleave', () => {
      button.style.transform = 'translateY(0) scale(1)';
    });
  });
}

// Handle search form submission
async function handleSearch(event) {
  event.preventDefault();
  
  if (isSearching) return;
  
  const country = countrySelect.value;
  const query = queryInput.value.trim();
  
  if (!country || !query) {
    showError('Please select a country and enter a product query.');
    return;
  }
  
  await performSearch(country, query);
}

// Enhanced search function with animations
async function performSearch(country, query) {
  try {
    isSearching = true;
    
    // Add searching animation class
    searchBtn.classList.add('searching');
    
    // Animate out previous results
    if (resultsGrid.children.length > 0) {
      Array.from(resultsGrid.children).forEach((card, index) => {
        setTimeout(() => {
          card.style.animation = 'slideOutDown 0.3s ease-in forwards';
        }, index * 50);
      });
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    showLoadingState();
    hideResults();
    
    // Simulate API delay with progress animation
    await animatedDelay(2000);
    
    const results = getSampleResults(country, query);
    hideLoadingState();
    displayResults(results, country, query);
    
  } catch (error) {
    console.error('Search error:', error);
    hideLoadingState();
    showError('An error occurred while searching. Please try again.');
  } finally {
    isSearching = false;
    searchBtn.classList.remove('searching');
  }
}

// Animated delay function
function animatedDelay(duration) {
  return new Promise(resolve => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 2;
      // Update progress indicator if you have one
      if (progress >= 100) {
        clearInterval(interval);
        resolve();
      }
    }, duration / 50);
  });
}

// Updated getSampleResults function to handle all products in all countries
function getSampleResults(country, query) {
  const queryLower = query.toLowerCase();
  
  // boAt Airdopes searches
  if (queryLower.includes('boat') || queryLower.includes('airdopes')) {
    return sampleData[`${country}_boAt`] || generateMockResults(country, query);
  }
  
  // iPhone searches
  if (queryLower.includes('iphone') && (queryLower.includes('16') || queryLower.includes('pro'))) {
    return sampleData[`${country}_iPhone`] || generateMockResults(country, query);
  }
  
  // Samsung Galaxy searches
  if (queryLower.includes('samsung') || queryLower.includes('galaxy') || queryLower.includes('s24')) {
    return sampleData[`${country}_Samsung`] || generateMockResults(country, query);
  }
  
  // Nintendo Switch searches
  if (queryLower.includes('nintendo') || queryLower.includes('switch')) {
    return sampleData[`${country}_Nintendo`] || generateMockResults(country, query);
  }
  
  return generateMockResults(country, query);
}

// Generate mock results for queries not in sample data
function generateMockResults(country, query) {
  const countryInfo = countries.find(c => c.code === country);
  const currency = countryInfo ? countryInfo.currency : 'USD';
  
  const vendors = {
    'US': ['Amazon', 'Best Buy', 'Walmart', 'Target'],
    'IN': ['Amazon India', 'Flipkart', 'Snapdeal', 'Myntra'],
    'UK': ['Amazon UK', 'Currys', 'Argos', 'John Lewis'],
    'JP': ['Amazon Japan', 'Rakuten', 'Yodobashi', 'Bic Camera']
  };
  
  const basePrice = Math.floor(Math.random() * 1000) + 100;
  const results = [];
  
  for (let i = 0; i < 3; i++) {
    const priceVariation = Math.floor(Math.random() * 200) - 100;
    const finalPrice = basePrice + priceVariation + (i * 50);
    
    results.push({
      productName: `${query} - ${vendors[country][i] || 'Local Store'}`,
      price: finalPrice.toFixed(2),
      currency: currency,
      vendor: vendors[country][i] || 'Local Store',
      link: '#',
      availability: 'in_stock'
    });
  }
  
  return results.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
}

// Show loading state with enhanced animations
function showLoadingState() {
  btnText.classList.add('hidden');
  btnSpinner.classList.remove('hidden');
  searchBtn.disabled = true;
  
  loadingSection.classList.remove('hidden');
  loadingSection.style.opacity = '0';
  loadingSection.style.transform = 'translateY(20px)';
  
  // Animate in loading section
  setTimeout(() => {
    loadingSection.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
    loadingSection.style.opacity = '1';
    loadingSection.style.transform = 'translateY(0)';
  }, 100);
}

// Hide loading state
function hideLoadingState() {
  btnText.classList.remove('hidden');
  btnSpinner.classList.add('hidden');
  searchBtn.disabled = false;
  
  loadingSection.style.opacity = '0';
  loadingSection.style.transform = 'translateY(-20px)';
  
  setTimeout(() => {
    loadingSection.classList.add('hidden');
  }, 300);
}

// Display search results with enhanced animations
function displayResults(results, country, query) {
  if (!results || results.length === 0) {
    showNoResults(query);
    return;
  }
  
  const sortedResults = [...results].sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
  
  // Update results header
  const countryInfo = countries.find(c => c.code === country);
  const countryName = countryInfo ? countryInfo.name : country;
  
  resultsTitle.textContent = `Results for "${query}" in ${countryName}`;
  resultsCount.textContent = `Found ${sortedResults.length} product${sortedResults.length !== 1 ? 's' : ''}`;
  
  // Clear previous results
  resultsGrid.innerHTML = '';
  
  // Create result cards with staggered animation
  sortedResults.forEach((result, index) => {
    const resultCard = createResultCard(result, index);
    resultsGrid.appendChild(resultCard);
  });
  
  // Show results section with animation
  resultsSection.classList.remove('hidden');
  resultsSection.style.opacity = '0';
  resultsSection.style.transform = 'translateY(30px)';
  
  setTimeout(() => {
    resultsSection.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    resultsSection.style.opacity = '1';
    resultsSection.style.transform = 'translateY(0)';
  }, 200);
  
  // Scroll to results with smooth animation
  setTimeout(() => {
    resultsSection.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'start' 
    });
  }, 800);
}

// Create a result card element with enhanced animations
function createResultCard(result, index) {
  const card = document.createElement('div');
  card.className = 'result-card';
  card.style.animationDelay = `${index * 0.1}s`;
  
  const availabilityClass = result.availability === 'in_stock' 
    ? 'result-availability--in-stock' 
    : result.availability === 'limited_stock'
    ? 'result-availability--limited-stock'
    : 'result-availability--out-of-stock';
  
  const availabilityText = result.availability === 'in_stock' 
    ? 'In Stock' 
    : result.availability === 'limited_stock'
    ? 'Limited Stock'
    : 'Out of Stock';
  
  // Format price with proper currency symbol
  const formattedPrice = formatPrice(result.price, result.currency);
  
  card.innerHTML = `
    <div class="result-header">
      <div class="result-price">
        ${formattedPrice}
        <span class="result-currency">${result.currency}</span>
      </div>
    </div>
    <h3 class="result-title">${result.productName}</h3>
    <div class="result-meta">
      <span class="result-vendor">${result.vendor}</span>
      <span class="result-availability ${availabilityClass}">${availabilityText}</span>
    </div>
    ${result.note ? `<div class="result-note">${result.note}</div>` : ''}
    <a href="${result.link}" class="result-link" target="_blank" rel="noopener noreferrer">
      ${result.link === '#' ? 'Contact Vendor' : 'View Product'}
    </a>
  `;
  
  // Add hover animations
  card.addEventListener('mouseenter', () => {
    card.style.transform = 'translateY(-8px) scale(1.02)';
  });
  
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'translateY(0) scale(1)';
  });
  
  return card;
}

// Format price with currency symbols
function formatPrice(price, currency) {
  const symbols = {
    'USD': '$',
    'INR': '₹',
    'GBP': '£',
    'JPY': '¥'
  };
  
  const symbol = symbols[currency] || currency;
  const numPrice = parseFloat(price);
  
  // Format based on currency
  if (currency === 'JPY') {
    return `${symbol}${Math.round(numPrice).toLocaleString()}`;
  } else if (currency === 'INR') {
    return `${symbol}${numPrice.toLocaleString('en-IN')}`;
  } else {
    return `${symbol}${numPrice.toFixed(2)}`;
  }
}

// Hide results section
function hideResults() {
  resultsSection.style.opacity = '0';
  resultsSection.style.transform = 'translateY(-20px)';
  
  setTimeout(() => {
    resultsSection.classList.add('hidden');
  }, 300);
}

// Show no results message
function showNoResults(query) {
  resultsTitle.textContent = `No results found for "${query}"`;
  resultsCount.textContent = 'Try different keywords or select another country';
  resultsGrid.innerHTML = `
    <div class="no-results" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
      <div style="font-size: 4rem; margin-bottom: 20px;">😔</div>
      <h3 style="margin-bottom: 12px; color: var(--color-text-primary);">No products found</h3>
      <p style="color: var(--color-text-secondary); margin: 0;">
        We couldn't find any products matching your search. Try different keywords or select another country.
      </p>
    </div>
  `;
  
  resultsSection.classList.remove('hidden');
  resultsSection.style.opacity = '0';
  resultsSection.style.transform = 'translateY(30px)';
  
  setTimeout(() => {
    resultsSection.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    resultsSection.style.opacity = '1';
    resultsSection.style.transform = 'translateY(0)';
  }, 200);
}

// Show error message
function showError(message) {
  // Create error notification
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-notification';
  errorDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    z-index: 1000;
    transform: translateX(100%);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-weight: 600;
  `;
  errorDiv.textContent = message;
  
  document.body.appendChild(errorDiv);
  
  // Animate in
  setTimeout(() => {
    errorDiv.style.transform = 'translateX(0)';
  }, 100);
  
  // Remove after 5 seconds
  setTimeout(() => {
    errorDiv.style.transform = 'translateX(100%)';
    setTimeout(() => {
      if (document.body.contains(errorDiv)) {
        document.body.removeChild(errorDiv);
      }
    }, 300);
  }, 5000);
}

// Add slideOutDown animation and additional styles
const style = document.createElement('style');
style.textContent = `
  @keyframes slideOutDown {
    from {
      opacity: 1;
      transform: translateY(0);
    }
    to {
      opacity: 0;
      transform: translateY(30px);
    }
  }
  
  .result-note {
    background: rgba(255, 193, 7, 0.1);
    color: #856404;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.85rem;
    margin: 12px 0;
    border-left: 3px solid #ffc107;
  }
  
  .result-availability--limited-stock {
    background: rgba(255, 193, 7, 0.1);
    color: #856404;
    border: 1px solid rgba(255, 193, 7, 0.3);
  }
  
  .result-availability--out-of-stock {
    background: rgba(220, 53, 69, 0.1);
    color: #721c24;
    border: 1px solid rgba(220, 53, 69, 0.3);
  }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    getSampleResults,
    generateMockResults,
    countries,
    sampleData,
    formatPrice
  };
}
