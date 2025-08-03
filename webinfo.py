# Import necessary modules from Flask and other libraries
from flask import Flask, render_template_string, request, jsonify, make_response, Response
import socket
import requests
import io
import random
import time

# Initialize the Flask application
app = Flask(__name__)

# The HTML template for the main homepage
HTML_HOMEPAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=0.45, shrink-to-fit=no">
    <title>Jojohn Web Info Scanner - Home</title>
    <!-- Tailwind CSS CDN for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Custom styles for animations and font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow: hidden;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
            animation: fadeIn 0.5s ease-out forwards;
        }
        .button-hover:hover {
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
            transform: translateY(-2px);
        }
        .button-active:active {
            transform: translateY(0);
        }
        .animated-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(220,38,38,0.2) 0%, rgba(26,26,26,0) 70%);
            animation: pulse 10s infinite;
            z-index: -1;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        @keyframes rotate-in {
            from { transform: rotateY(0deg); opacity: 0; }
            to { transform: rotateY(360deg); opacity: 1; }
        }
        .icon-animation {
            animation: rotate-in 1s ease-out;
        }
        @keyframes fade-in-down {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in-down-icon {
            animation: fade-in-down 0.8s ease-out forwards;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 flex flex-col min-h-screen">
    <div class="animated-background"></div>

    <!-- Navigation Header -->
    <header class="bg-gray-800 p-4 shadow-lg sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-xl md:text-2xl font-extrabold text-red-500 flex items-center">
                <i class="fa-solid fa-signal text-red-500 mr-2 fade-in-down-icon"></i>
                Jojohn Web Info Scanner
            </h1>
            <nav class="flex gap-4">
                <a href="/" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Home</a>
                <a href="/scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Scanner</a>
                <a href="/geolocation-scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Geolocation Scanner</a>
                <a href="/speedtest" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Speed Test</a>
                <a href="/contact" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Contact</a>
            </nav>
        </div>
    </header>

    <!-- Main content for the homepage -->
    <main class="flex-grow flex items-center justify-center p-4">
        <div class="text-center animate-fadeIn max-w-2xl mx-auto p-4 sm:p-8 md:p-12">
            <h2 class="text-3xl md:text-5xl font-extrabold text-white mb-4">Discover Website Details Instantly</h2>
            <p class="text-base md:text-lg text-gray-400 mb-8">
                Jojohn Web Info Scanner tool provides you with crucial information about any website, including its IP address, geographical location, and hosting details. It's a simple, fast, and powerful way to gain insights.
            </p>
            <a href="/scanner" class="button-hover button-active bg-red-600 text-white font-bold py-3 px-6 md:py-4 md:px-8 rounded-full shadow-lg transition-all duration-300 ease-in-out inline-flex items-center gap-2">
                <i class="fa-solid fa-arrow-right-to-bracket icon-animation"></i>
                <span>Get Started</span>
            </a>
        </div>
    </main>
</body>
</html>
"""

# The HTML template for the web page, including CSS and JavaScript for the general scanner page.
HTML_SCANNER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jojohn Web Info Scanner</title>
    <!-- Tailwind CSS CDN for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Custom styles for animations and font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
            animation: fadeIn 0.5s ease-out forwards;
        }
        .spinning {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .button-hover:hover {
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
            transform: translateY(-2px);
        }
        .button-active:active {
            transform: translateY(0);
        }
        .animated-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(220,38,38,0.2) 0%, rgba(26,26,26,0) 70%);
            animation: pulse 10s infinite;
            z-index: -1;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        @keyframes slide-in {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .icon-slide-in {
            animation: slide-in 0.5s ease-out;
        }
        @keyframes bounce-in {
            0% { transform: scale(0); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); }
        }
        .icon-bounce-in {
            animation: bounce-in 0.7s ease-out;
        }
        @keyframes fade-in-down {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in-down-icon {
            animation: fade-in-down 0.8s ease-out forwards;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 flex flex-col min-h-screen">
    <div class="animated-background"></div>

    <!-- Navigation Header -->
    <header class="bg-gray-800 p-4 shadow-lg sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-xl md:text-2xl font-extrabold text-red-500 flex items-center">
                <i class="fa-solid fa-signal text-red-500 mr-2 fade-in-down-icon"></i>
                Jojohn Web Info Scanner
            </h1>
            <nav class="flex gap-4">
                <a href="/" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Home</a>
                <a href="/scanner" class="text-red-500 font-bold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200 border-b-2 border-red-500">Scanner</a>
                <a href="/geolocation-scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Geolocation Scanner</a>
                <a href="/speedtest" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Speed Test</a>
                <a href="/contact" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Contact</a>
            </nav>
        </div>
    </header>
    
    <!-- Main content for the scanner -->
    <main class="flex-grow flex items-center justify-center p-4">
        <div class="bg-gray-800 p-4 sm:p-8 md:p-12 rounded-2xl shadow-xl max-w-lg md:max-w-6xl w-full text-center border border-gray-700 relative z-10 animate-fadeIn">
            <!-- Section for the Info Scanner -->
            <div class="bg-gray-700/50 p-4 sm:p-6 rounded-xl border border-gray-600">
                <h2 class="text-xl md:text-2xl font-bold text-white mb-4">
                    <i class="fa-solid fa-satellite-dish text-red-500 mr-2 icon-slide-in"></i>
                    Scan a Website
                </h2>
                <p class="text-sm md:text-base text-gray-400 mb-6">Enter a website URL to get its IP address and geographical information.</p>
                
                <form id="scan-form" class="flex flex-col gap-8">
                    <div class="relative">
                        <i class="fa-solid fa-globe absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"></i>
                        <input 
                            type="text" 
                            id="website-url" 
                            placeholder="Enter website URL (e.g., example.com)" 
                            required 
                            class="w-full pl-12 pr-4 py-3 bg-gray-700 text-white border-2 border-gray-600 rounded-xl focus:border-red-500 focus:ring-4 focus:ring-red-900 transition-all duration-300 outline-none"
                        >
                    </div>
                    <button 
                        type="submit" 
                        class="button-hover button-active w-full py-4 bg-red-600 text-white font-bold rounded-xl flex items-center justify-center gap-2 transition-all duration-300 ease-in-out"
                    >
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <span>Scan Website</span>
                    </button>
                </form>
            </div>
            
            <div class="flex flex-col md:flex-row gap-8 mt-8 md:items-stretch items-center">
                <div id="results-container" class="flex-1">
                    <!-- Loading indicator, error message, and results will be injected here by JS -->
                    <div id="loading-indicator" class="hidden text-center">
                        <i class="fa-solid fa-spinner fa-3x text-red-500 spinning"></i>
                        <p class="mt-4 text-gray-400 font-semibold">Scanning...</p>
                    </div>
                    
                    <div id="error-message" class="hidden bg-red-900/20 text-red-400 p-4 rounded-xl border border-red-800">
                        <i class="fa-solid fa-triangle-exclamation mr-2"></i>
                        <span class="font-semibold">Error: Could not retrieve information for the provided URL.</span>
                    </div>
                    
                    <div id="results-content" class="text-left hidden animate-fadeIn bg-gray-700 p-6 rounded-xl border border-gray-600 h-full">
                        <!-- Results will be injected here -->
                    </div>
                </div>
                
                <div id="map-container" class="flex-1 hidden animate-fadeIn">
                    <h4 class="text-xl font-bold text-gray-300 mb-2">Location on Map</h4>
                    <div class="rounded-xl overflow-hidden border border-gray-700 shadow-sm">
                        <iframe id="map" class="w-full h-64 md:h-80" src="" allowfullscreen="" loading="lazy"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        // Get references to the HTML elements
        const form = document.getElementById('scan-form');
        const urlInput = document.getElementById('website-url');
        const resultsContent = document.getElementById('results-content');
        const loadingIndicator = document.getElementById('loading-indicator');
        const errorMessage = document.getElementById('error-message');
        const mapContainer = document.getElementById('map-container');
        const mapIframe = document.getElementById('map');

        // Add a listener for the form submission event
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent the default form submission
            
            const websiteUrl = urlInput.value.trim();

            // Clear previous results and show loading indicator
            resultsContent.innerHTML = '';
            resultsContent.classList.add('hidden');
            errorMessage.classList.add('hidden');
            mapContainer.classList.add('hidden');
            loadingIndicator.classList.remove('hidden');

            try {
                // Fetch data from our Flask backend endpoint
                const response = await fetch('/scan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: websiteUrl })
                });

                // Check if the response was successful
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                
                // Parse the JSON response
                const data = await response.json();

                // Check for errors in the response data
                if (data.error) {
                    throw new Error(data.error);
                }

                // Construct the output string with the results
                let output = '';
                output += '<h3 class="text-xl font-bold text-gray-300 mb-4 flex items-center gap-2"><i class="fa-solid fa-circle-info text-red-500 icon-bounce-in"></i> Scan Results</h3>';
                for (const [key, value] of Object.entries(data)) {
                    // Skip lat/lon from the main list if they exist, as they're for the map
                    if (key !== 'Latitude' && key !== 'Longitude') {
                        output += `<p class="mb-2"><span class="font-semibold text-gray-400">${key}:</span> <span class="text-gray-100">${value}</span></p>`;
                    }
                }
                resultsContent.innerHTML = output;
                resultsContent.classList.remove('hidden');

                // Update the map
                if (data.Latitude && data.Longitude && data.Latitude !== 'N/A' && data.Longitude !== 'N/A' && !isNaN(data.Latitude) && !isNaN(data.Longitude)) {
                    const lat = parseFloat(data.Latitude);
                    const lon = parseFloat(data.Longitude);
                    // Use a more reliable map embed URL
                    mapIframe.src = `https://maps.google.com/maps?q=${lat},${lon}&hl=en&z=14&output=embed`;
                    mapContainer.classList.remove('hidden');
                } else {
                    mapContainer.classList.add('hidden');
                }

            } catch (error) {
                console.error('Error:', error);
                errorMessage.classList.remove('hidden');
                resultsContent.innerHTML = `<p class="mt-4 text-center text-gray-400">Please try a different URL.</p>`;
                resultsContent.classList.remove('hidden');
            } finally {
                // Hide the loading indicator regardless of success or failure
                loadingIndicator.classList.add('hidden');
            }
        });
    </script>
</body>
</html>
"""

# The HTML template for the dedicated geolocation scanner page.
HTML_GEOLOCATION_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Geolocation Scanner</title>
    <!-- Tailwind CSS CDN for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Custom styles for animations and font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
            animation: fadeIn 0.5s ease-out forwards;
        }
        .spinning {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .button-hover:hover {
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
            transform: translateY(-2px);
        }
        .button-active:active {
            transform: translateY(0);
        }
        .animated-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(220,38,38,0.2) 0%, rgba(26,26,26,0) 70%);
            animation: pulse 10s infinite;
            z-index: -1;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        @keyframes slide-in {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .icon-slide-in {
            animation: slide-in 0.5s ease-out;
        }
        @keyframes bounce-in {
            0% { transform: scale(0); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); }
        }
        .icon-bounce-in {
            animation: bounce-in 0.7s ease-out;
        }
        @keyframes fade-in-down {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in-down-icon {
            animation: fade-in-down 0.8s ease-out forwards;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 flex flex-col min-h-screen">
    <div class="animated-background"></div>

    <!-- Navigation Header -->
    <header class="bg-gray-800 p-4 shadow-lg sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-xl md:text-2xl font-extrabold text-red-500 flex items-center">
                <i class="fa-solid fa-signal text-red-500 mr-2 fade-in-down-icon"></i>
                Jojohn Web Info Scanner
            </h1>
            <nav class="flex gap-4">
                <a href="/" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Home</a>
                <a href="/scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Scanner</a>
                <a href="/geolocation-scanner" class="text-red-500 font-bold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200 border-b-2 border-red-500">Geolocation Scanner</a>
                <a href="/speedtest" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Speed Test</a>
                <a href="/contact" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Contact</a>
            </nav>
        </div>
    </header>
    
    <!-- Main content for the scanner -->
    <main class="flex-grow flex items-center justify-center p-4">
        <div class="bg-gray-800 p-4 sm:p-8 md:p-12 rounded-2xl shadow-xl max-w-4xl w-full text-center border border-gray-700 relative z-10 animate-fadeIn">
            <!-- Section for the Info Scanner -->
            <div class="bg-gray-700/50 p-4 sm:p-6 rounded-xl border border-gray-600">
                <h2 class="text-xl md:text-2xl font-bold text-white mb-4">
                    <i class="fa-solid fa-map-location-dot text-red-500 mr-2 icon-slide-in"></i>
                    URL Geolocation Scanner
                </h2>
                <p class="text-sm md:text-base text-gray-400 mb-6">Enter a website URL to get its IP address and geographical location on a map.</p>
                
                <form id="scan-form" class="flex flex-col gap-8">
                    <div class="relative">
                        <i class="fa-solid fa-globe absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"></i>
                        <input 
                            type="text" 
                            id="website-url" 
                            placeholder="Enter website URL (e.g., example.com)" 
                            required 
                            class="w-full pl-12 pr-4 py-3 bg-gray-700 text-white border-2 border-gray-600 rounded-xl focus:border-red-500 focus:ring-4 focus:ring-red-900 transition-all duration-300 outline-none"
                        >
                    </div>
                    <button 
                        type="submit" 
                        class="button-hover button-active w-full py-4 bg-red-600 text-white font-bold rounded-xl flex items-center justify-center gap-2 transition-all duration-300 ease-in-out"
                    >
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <span>Scan Website</span>
                    </button>
                </form>
            </div>
            
            <div id="results-container" class="mt-8 hidden animate-fadeIn">
                <!-- Loading indicator, error message, and results will be injected here by JS -->
                <div id="loading-indicator" class="hidden text-center">
                    <i class="fa-solid fa-spinner fa-3x text-red-500 spinning"></i>
                    <p class="mt-4 text-gray-400 font-semibold">Scanning...</p>
                </div>
                
                <div id="error-message" class="hidden bg-red-900/20 text-red-400 p-4 rounded-xl border border-red-800">
                    <i class="fa-solid fa-triangle-exclamation mr-2"></i>
                    <span class="font-semibold">Error: Could not retrieve information for the provided URL.</span>
                </div>
                
                <div id="address-container" class="text-left hidden animate-fadeIn bg-gray-700 p-6 rounded-xl border border-gray-600 mb-8">
                    <h3 class="text-xl font-bold text-gray-300 mb-4 flex items-center gap-2"><i class="fa-solid fa-location-dot text-red-500 icon-bounce-in"></i> Geolocation Address</h3>
                    <p id="address-text" class="text-gray-100 text-lg"></p>
                </div>

                <div id="map-container" class="hidden animate-fadeIn">
                    <h4 class="text-xl font-bold text-gray-300 mb-2">Location on Map</h4>
                    <div class="rounded-xl overflow-hidden border border-gray-700 shadow-sm">
                        <iframe id="map" class="w-full h-64 md:h-80" src="" allowfullscreen="" loading="lazy"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        // Get references to the HTML elements
        const form = document.getElementById('scan-form');
        const urlInput = document.getElementById('website-url');
        const resultsContainer = document.getElementById('results-container');
        const loadingIndicator = document.getElementById('loading-indicator');
        const errorMessage = document.getElementById('error-message');
        const addressContainer = document.getElementById('address-container');
        const addressText = document.getElementById('address-text');
        const mapContainer = document.getElementById('map-container');
        const mapIframe = document.getElementById('map');

        // Add a listener for the form submission event
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent the default form submission
            
            const websiteUrl = urlInput.value.trim();

            // Clear previous results and show loading indicator
            addressText.innerHTML = '';
            resultsContainer.classList.add('hidden');
            errorMessage.classList.add('hidden');
            addressContainer.classList.add('hidden');
            mapContainer.classList.add('hidden');
            loadingIndicator.classList.remove('hidden');

            try {
                // Fetch data from our Flask backend endpoint
                const response = await fetch('/scan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: websiteUrl })
                });

                // Check if the response was successful
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                
                // Parse the JSON response
                const data = await response.json();

                // Check for errors in the response data
                if (data.error) {
                    throw new Error(data.error);
                }

                // Show the main results container
                resultsContainer.classList.remove('hidden');

                // Update the address display
                if (data.City || data.Region || data.Country) {
                    const addressParts = [data.City, data.Region, data.Country].filter(part => part && part !== 'N/A');
                    addressText.textContent = addressParts.join(', ');
                    addressContainer.classList.remove('hidden');
                } else {
                    addressContainer.classList.add('hidden');
                }

                // Update the map
                if (data.Latitude && data.Longitude && data.Latitude !== 'N/A' && data.Longitude !== 'N/A' && !isNaN(data.Latitude) && !isNaN(data.Longitude)) {
                    const lat = parseFloat(data.Latitude);
                    const lon = parseFloat(data.Longitude);
                    // Use a more reliable map embed URL
                    mapIframe.src = `https://maps.google.com/maps?q=${lat},${lon}&hl=en&z=14&output=embed`;
                    mapContainer.classList.remove('hidden');
                } else {
                    mapContainer.classList.add('hidden');
                }

            } catch (error) {
                console.error('Error:', error);
                errorMessage.classList.remove('hidden');
            } finally {
                // Hide the loading indicator regardless of success or failure
                loadingIndicator.classList.add('hidden');
            }
        });
    </script>
</body>
</html>
"""

# The HTML template for the new speed test page.
HTML_SPEEDTEST_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Internet Speed Test</title>
    <!-- Tailwind CSS CDN for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Custom styles for animations and font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
            animation: fadeIn 0.5s ease-out forwards;
        }
        .spinning {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .button-hover:hover {
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
            transform: translateY(-2px);
        }
        .button-active:active {
            transform: translateY(0);
        }
        .animated-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(220,38,38,0.2) 0%, rgba(26,26,26,0) 70%);
            animation: pulse 10s infinite;
            z-index: -1;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        @keyframes slide-in {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .icon-slide-in {
            animation: slide-in 0.5s ease-out;
        }
        @keyframes bounce-in {
            0% { transform: scale(0); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); }
        }
        .icon-bounce-in {
            animation: bounce-in 0.7s ease-out;
        }
        @keyframes fade-in-down {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in-down-icon {
            animation: fade-in-down 0.8s ease-out forwards;
        }

        /* Speed Meter Specific Styles */
        .meter-container {
            position: relative;
            width: 250px;
            height: 125px;
            margin: 0 auto;
            overflow: hidden;
        }
        .meter-background {
            position: absolute;
            width: 250px;
            height: 250px;
            border-radius: 50%;
            background: conic-gradient(from 135deg, transparent 0deg 45deg, #4b5563 45deg 135deg, transparent 135deg 180deg);
        }
        .meter-fill {
            position: absolute;
            width: 250px;
            height: 250px;
            border-radius: 50%;
            background: conic-gradient(from 135deg, transparent 0deg 45deg, #ef4444 45deg 135deg, transparent 135deg 180deg);
            clip-path: polygon(0% 100%, 100% 100%, 50% 50%);
            transform-origin: 50% 50%;
            transform: rotate(0deg);
            transition: transform 0.5s ease-out;
        }
        .meter-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 flex flex-col min-h-screen">
    <div class="animated-background"></div>

    <!-- Navigation Header -->
    <header class="bg-gray-800 p-4 shadow-lg sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-xl md:text-2xl font-extrabold text-red-500 flex items-center">
                <i class="fa-solid fa-signal text-red-500 mr-2 fade-in-down-icon"></i>
                Jojohn Web Info Scanner
            </h1>
            <nav class="flex gap-4">
                <a href="/" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Home</a>
                <a href="/scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Scanner</a>
                <a href="/geolocation-scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Geolocation Scanner</a>
                <a href="/speedtest" class="text-red-500 font-bold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200 border-b-2 border-red-500">Speed Test</a>
                <a href="/contact" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Contact</a>
            </nav>
        </div>
    </header>
    
    <!-- Main content for the speed test -->
    <main class="flex-grow flex items-center justify-center p-4">
        <div class="bg-gray-800 p-4 sm:p-8 md:p-12 rounded-2xl shadow-xl max-w-4xl w-full text-center border border-gray-700 relative z-10 animate-fadeIn">
            <div class="bg-gray-700/50 p-4 sm:p-6 rounded-xl border border-gray-600">
                <h2 class="text-xl md:text-2xl font-bold text-white mb-4">
                    <i class="fa-solid fa-tachometer-alt text-red-500 mr-2 icon-slide-in"></i>
                    Internet Speed Test
                </h2>
                <p id="status-message" class="text-sm md:text-base text-gray-400 mb-6">Click "Start Test" to measure your connection speed.</p>
                
                <div class="relative w-full h-auto flex flex-col items-center justify-center mb-8">
                    <div class="meter-container">
                        <div class="meter-background"></div>
                        <div id="meter-fill" class="meter-fill"></div>
                        <div class="meter-text absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                            <p id="meter-value" class="text-4xl font-bold text-white">0.00</p>
                            <p id="meter-unit" class="text-sm text-gray-400">Mbps</p>
                        </div>
                    </div>
                </div>

                <div id="results-display" class="flex flex-col md:flex-row justify-around items-center my-8 gap-6">
                    <div class="bg-gray-700 p-6 rounded-xl flex-1 w-full md:w-auto border border-gray-600 shadow-md">
                        <i id="ping-icon" class="fa-solid fa-arrows-alt-h text-gray-400 text-3xl mb-2"></i>
                        <h4 class="text-lg font-semibold text-gray-300">Ping</h4>
                        <p id="ping-result" class="text-3xl md:text-4xl font-bold text-white mt-2">- ms</p>
                    </div>
                    <div class="bg-gray-700 p-6 rounded-xl flex-1 w-full md:w-auto border border-gray-600 shadow-md">
                        <i id="download-icon" class="fa-solid fa-download text-gray-400 text-3xl mb-2"></i>
                        <h4 class="text-lg font-semibold text-gray-300">Download</h4>
                        <p id="download-result" class="text-3xl md:text-4xl font-bold text-white mt-2">- Mbps</p>
                    </div>
                    <div class="bg-gray-700 p-6 rounded-xl flex-1 w-full md:w-auto border border-gray-600 shadow-md">
                        <i id="upload-icon" class="fa-solid fa-upload text-gray-400 text-3xl mb-2"></i>
                        <h4 class="text-lg font-semibold text-gray-300">Upload</h4>
                        <p id="upload-result" class="text-3xl md:text-4xl font-bold text-white mt-2">- Mbps</p>
                    </div>
                </div>

                <button 
                    id="start-test-button" 
                    class="button-hover button-active w-full py-4 bg-red-600 text-white font-bold rounded-xl flex items-center justify-center gap-2 transition-all duration-300 ease-in-out"
                >
                    <i class="fa-solid fa-play"></i>
                    <span>Start Test</span>
                </button>
            </div>
        </div>
    </main>

    <script>
        // Get references to all the HTML elements
        const startTestButton = document.getElementById('start-test-button');
        const statusMessage = document.getElementById('status-message');
        
        const pingResult = document.getElementById('ping-result');
        const downloadResult = document.getElementById('download-result');
        const uploadResult = document.getElementById('upload-result');
        
        const pingIcon = document.getElementById('ping-icon');
        const downloadIcon = document.getElementById('download-icon');
        const uploadIcon = document.getElementById('upload-icon');
        
        const meterValue = document.getElementById('meter-value');
        const meterUnit = document.getElementById('meter-unit');
        const meterFill = document.getElementById('meter-fill');

        // Configuration variables for the test
        const PING_COUNT = 5;
        const DOWNLOAD_FILE_SIZE_MB = 10; // Size of the test file for download
        const UPLOAD_DATA_SIZE_MB = 2; // Size of the test data for upload
        const MAX_METER_SPEED_MBPS = 200; // Max speed for the meter's display range

        // Reset the UI to its initial state
        function resetUI() {
            statusMessage.textContent = 'Click "Start Test" to measure your connection speed.';
            pingResult.textContent = '- ms';
            downloadResult.textContent = '- Mbps';
            uploadResult.textContent = '- Mbps';
            pingIcon.classList.remove('text-red-500', 'spinning');
            downloadIcon.classList.remove('text-red-500', 'spinning');
            uploadIcon.classList.remove('text-red-500', 'spinning');
            pingIcon.classList.add('text-gray-400');
            downloadIcon.classList.add('text-gray-400');
            uploadIcon.classList.add('text-gray-400');
            startTestButton.disabled = false;
            startTestButton.innerHTML = '<i class="fa-solid fa-play"></i><span>Start Test</span>';
            updateMeter(0);
        }
        
        // Update the speed meter display
        function updateMeter(speedMbps) {
            const cappedSpeed = Math.min(speedMbps, MAX_METER_SPEED_MBPS);
            const rotation = (cappedSpeed / MAX_METER_SPEED_MBPS) * 180;
            meterFill.style.transform = `rotate(${rotation}deg)`;
            meterValue.textContent = speedMbps.toFixed(2);
        }

        // Function to perform the ping test
        async function pingTest() {
            statusMessage.textContent = 'Testing Ping...';
            pingIcon.classList.remove('text-gray-400');
            pingIcon.classList.add('text-red-500', 'spinning');
            
            let totalTime = 0;
            const testUrl = '/speedtest'; // Use a local URL to reduce external network latency
            const pingTimestamps = [];
            for (let i = 0; i < PING_COUNT; i++) {
                const startPingTime = performance.now();
                await fetch(testUrl, { cache: 'no-store' });
                const endPingTime = performance.now();
                pingTimestamps.push(endPingTime - startPingTime);
            }
            const avgPing = pingTimestamps.reduce((sum, time) => sum + time, 0) / PING_COUNT;
            
            pingResult.textContent = `${avgPing.toFixed(0)} ms`;
            pingIcon.classList.remove('spinning');
            return avgPing;
        }

        // Function to perform the download speed test
        async function downloadTest() {
            statusMessage.textContent = 'Testing Download Speed...';
            downloadIcon.classList.remove('text-gray-400');
            downloadIcon.classList.add('text-red-500', 'spinning');
            
            const testUrl = `/api/download?size=${DOWNLOAD_FILE_SIZE_MB}`;
            const startTime = performance.now();
            
            const response = await fetch(testUrl, { cache: 'no-store' });
            if (!response.ok) {
                throw new Error('Download test failed');
            }

            const reader = response.body.getReader();
            let receivedBytes = 0;
            let lastUpdate = performance.now();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                receivedBytes += value.length;
                const currentTime = performance.now();
                const timeElapsed = (currentTime - startTime) / 1000;
                
                // Update the meter more frequently
                if (currentTime - lastUpdate > 200) {
                    const currentSpeedMbps = (receivedBytes * 8) / (1000 * 1000) / timeElapsed;
                    updateMeter(currentSpeedMbps);
                    lastUpdate = currentTime;
                }
            }
            
            const endTime = performance.now();
            const totalTimeSeconds = (endTime - startTime) / 1000;
            const totalBits = receivedBytes * 8;
            const finalSpeedMbps = (totalBits / totalTimeSeconds) / 1000000;

            downloadResult.textContent = `${finalSpeedMbps.toFixed(2)} Mbps`;
            downloadIcon.classList.remove('spinning');
            return finalSpeedMbps;
        }

        // Function to perform the upload speed test
        async function uploadTest() {
            statusMessage.textContent = 'Testing Upload Speed...';
            uploadIcon.classList.remove('text-gray-400');
            uploadIcon.classList.add('text-red-500', 'spinning');
            
            // Generate a large data blob for the upload test
            const uploadData = new Blob([new Array(UPLOAD_DATA_SIZE_MB * 1024 * 1024).fill('a').join('')]);
            
            const uploadUrl = '/api/upload';
            const startTime = performance.now();

            // Simulate the meter updating during the upload process
            const fakeMeterInterval = setInterval(() => {
                const currentTime = performance.now();
                const timeElapsed = (currentTime - startTime) / 1000;
                // A very simple estimate of speed
                if (timeElapsed > 0) {
                    const estimatedSpeed = (UPLOAD_DATA_SIZE_MB * 8) / timeElapsed;
                    updateMeter(estimatedSpeed);
                }
            }, 200);
            
            const response = await fetch(uploadUrl, {
                method: 'POST',
                body: uploadData,
                headers: {
                    'Content-Type': 'application/octet-stream'
                },
                cache: 'no-store'
            });
            
            clearInterval(fakeMeterInterval);
            const endTime = performance.now();
            
            if (!response.ok) {
                throw new Error('Upload test failed');
            }
            
            const durationSeconds = (endTime - startTime) / 1000;
            const dataSizeBits = UPLOAD_DATA_SIZE_MB * 1024 * 1024 * 8;
            const finalSpeedMbps = (dataSizeBits / durationSeconds) / 1000000;
            
            uploadResult.textContent = `${finalSpeedMbps.toFixed(2)} Mbps`;
            updateMeter(finalSpeedMbps);
            uploadIcon.classList.remove('spinning');
            return finalSpeedMbps;
        }


        // The main function to run all tests sequentially
        async function runSpeedTest() {
            startTestButton.disabled = true;
            startTestButton.innerHTML = '<i class="fa-solid fa-spinner spinning"></i><span>Testing...</span>';
            
            resetUI();
            
            try {
                // Step 1: Ping Test
                await pingTest();

                // Step 2: Download Test
                await downloadTest();

                // Step 3: Upload Test
                await uploadTest();

                // All tests finished
                statusMessage.textContent = 'Test complete!';
                startTestButton.innerHTML = '<i class="fa-solid fa-check"></i><span>Test Again</span>';
                
            } catch (error) {
                console.error('Speed test error:', error);
                statusMessage.textContent = 'An error occurred. Please try again.';
                updateMeter(0);
                startTestButton.innerHTML = '<i class="fa-solid fa-exclamation-triangle"></i><span>Test Failed</span>';
            } finally {
                startTestButton.disabled = false;
            }
        }
        
        // Event listener for the "Start Test" button
        startTestButton.addEventListener('click', runSpeedTest);
        
        // Initial setup
        resetUI();
    </script>
</body>
</html>
"""

# The HTML template for the contact page
HTML_CONTACT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jojoh Web Info Scanner - Contact</title>
    <!-- Tailwind CSS CDN for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Custom styles for animations and font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
            animation: fadeIn 0.5s ease-out forwards;
        }
        .button-hover:hover {
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
            transform: translateY(-2px);
        }
        .button-active:active {
            transform: translateY(0);
        }
        .animated-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(220,38,38,0.2) 0%, rgba(26,26,26,0) 70%);
            animation: pulse 10s infinite;
            z-index: -1;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        @keyframes fade-in-down {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in-down-icon {
            animation: fade-in-down 0.8s ease-out forwards;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 flex flex-col min-h-screen">
    <div class="animated-background"></div>

    <!-- Navigation Header -->
    <header class="bg-gray-800 p-4 shadow-lg sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-xl md:text-2xl font-extrabold text-red-500 flex items-center">
                <i class="fa-solid fa-signal text-red-500 mr-2 fade-in-down-icon"></i>
                Jojohn Web Info Scanner
            </h1>
            <nav class="flex gap-4">
                <a href="/" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Home</a>
                <a href="/scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Scanner</a>
                <a href="/geolocation-scanner" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Geolocation Scanner</a>
                <a href="/speedtest" class="text-gray-300 hover:text-red-500 font-semibold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200">Speed Test</a>
                <a href="/contact" class="text-red-500 font-bold px-2 md:px-4 py-2 rounded-lg transition-colors duration-200 border-b-2 border-red-500">Contact</a>
            </nav>
        </div>
    </header>
    
    <!-- Main content for the contact page -->
    <main class="flex-grow flex items-center justify-center p-4">
        <div class="bg-gray-800 p-4 sm:p-8 md:p-12 rounded-2xl shadow-xl max-w-lg w-full text-center border border-gray-700 relative z-10 animate-fadeIn">
            <h2 class="text-2xl md:text-3xl font-bold text-white mb-4">Contact Information</h2>
            <p class="text-sm md:text-base text-gray-400 mb-6">Feel free to reach out using the details below.</p>

            <div class="flex flex-col gap-6 text-left">
                <div class="flex items-center gap-4 p-4 bg-gray-700/50 rounded-xl border border-gray-600">
                    <i class="fa-solid fa-envelope text-red-500 text-2xl"></i>
                    <div>
                        <h4 class="text-gray-300 font-semibold">Email Address</h4>
                        <p class="text-white">jomerjohnvalmoriaalavarado@gmail.com</p>
                    </div>
                </div>
                <div class="flex items-center gap-4 p-4 bg-gray-700/50 rounded-xl border border-gray-600">
                    <i class="fa-solid fa-phone text-red-500 text-2xl"></i>
                    <div>
                        <h4 class="text-gray-300 font-semibold">Contact Number</h4>
                        <p class="text-white">+63 (9750478871)</p>
                    </div>
                </div>
                <div class="flex items-center gap-4 p-4 bg-gray-700/50 rounded-xl border border-gray-600">
                    <i class="fa-solid fa-location-dot text-red-500 text-2xl"></i>
                    <div>
                        <h4 class="text-gray-300 font-semibold">Location</h4>
                        <p class="text-white">Baybay, Liloy, Zamboanga Del Norte, 7115</p>
                    </div>
                </div>
            </div>
        </div>
    </main>
</body>
</html>
"""


# Define the main route for the homepage
@app.route('/')
def home():
    """
    Renders the HTML template for the main homepage.
    """
    return render_template_string(HTML_HOMEPAGE_TEMPLATE)

# Define the route for the general scanner page
@app.route('/scanner')
def scanner():
    """
    Renders the HTML template for the general scanner tool page.
    """
    return render_template_string(HTML_SCANNER_TEMPLATE)

# Define the route for the dedicated geolocation scanner page
@app.route('/geolocation-scanner')
def geolocation_scanner():
    """
    Renders the HTML template for the dedicated geolocation scanner page.
    """
    return render_template_string(HTML_GEOLOCATION_TEMPLATE)

# Define the route for the new speed test page
@app.route('/speedtest')
def speedtest():
    """
    Renders the HTML template for the speed test page.
    """
    return render_template_string(HTML_SPEEDTEST_TEMPLATE)

# Define the route for the contact page
@app.route('/contact')
def contact():
    """
    Renders the HTML template for the contact page.
    """
    return render_template_string(HTML_CONTACT_TEMPLATE)


# Define the API endpoint for scanning a website
@app.route('/scan', methods=['POST'])
def scan_website():
    """
    Handles the website scanning logic.
    - Gets the URL from the JSON body of the request.
    - Resolves the IP address using the socket module.
    - Uses a third-party API (ip-api.com) to get more information about the IP.
    - Returns a JSON response with the IP and other details.
    """
    try:
        # Get the URL from the JSON body of the request
        data = request.get_json()
        website_url = data.get('url')

        if not website_url:
            return jsonify({'error': 'URL is required'}), 400

        # Remove 'http://' or 'https://' from the URL for DNS lookup
        hostname = website_url.replace('http://', '').replace('https://', '').split('/')[0]

        # Use the socket module to get the IP address
        try:
            ip_address = socket.gethostbyname(hostname)
        except socket.gaierror:
            return jsonify({'error': f'Could not resolve IP address for {website_url}'}), 400

        # Use a free public API to get information about the IP address
        # The 'requests' library is used for making HTTP requests
        # Note: You can replace this with any other IP lookup service.
        api_url = f'http://ip-api.com/json/{ip_address}'
        response = requests.get(api_url)
        ip_info = response.json()

        # Combine the information into a single dictionary
        results = {
            'Domain': hostname,
            'IP Address': ip_address,
            'Country': ip_info.get('country', 'N/A'),
            'Region': ip_info.get('regionName', 'N/A'),
            'City': ip_info.get('city', 'N/A'),
            'ISP': ip_info.get('isp', 'N/A'),
            'Hosting Organization': ip_info.get('org', 'N/A'),
            'AS (Autonomous System)': ip_info.get('as', 'N/A'),
            'Latitude': ip_info.get('lat', 'N/A'),
            'Longitude': ip_info.get('lon', 'N/A'),
        }

        # Return the results as a JSON response
        return jsonify(results)

    except Exception as e:
        # Handle any unexpected errors and return a generic error message
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

# Define a new API endpoint for the speed test download
@app.route('/api/download')
def download_test_api():
    """
    An endpoint to serve a large, randomly generated file for a download test.
    The size of the file is controlled by the 'size' query parameter in MB.
    """
    try:
        size_mb = int(request.args.get('size', 10))
        size_bytes = size_mb * 1024 * 1024  # Convert MB to bytes

        # Generate random data in chunks to avoid high memory usage
        def generate_data():
            chunk_size = 1024 * 1024  # 1MB chunks
            for _ in range(size_mb):
                yield b'\x00' * chunk_size
                time.sleep(0.01) # Small delay to simulate real network conditions

        response = Response(generate_data(), mimetype='application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename=testfile_{size_mb}mb.dat'
        response.headers['Content-Length'] = size_bytes
        return response
    except Exception as e:
        print(f"Download API error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Define a new API endpoint for the speed test upload
@app.route('/api/upload', methods=['POST'])
def upload_test_api():
    """
    A simple endpoint to handle upload tests.
    It receives data and simply returns a success response.
    The time measurement is done on the client side (in JavaScript).
    """
    try:
        # We don't need to process the data, just confirm receipt.
        # This is enough for the client to calculate upload speed.
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Upload API error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
