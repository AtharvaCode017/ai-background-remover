# 🎨 AI Background Remover

A simple, powerful web application that removes image backgrounds using artificial intelligence. Built with Python Flask and powered by the rembg library.


## ✨ Features

- **🤖 AI-Powered**: Uses advanced machine learning models for accurate background removal
- **🖱️ Drag & Drop**: Intuitive file upload with drag-and-drop support
- **📱 Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **⚡ Fast Processing**: Remove backgrounds in seconds
- **📁 Multiple Formats**: Supports JPG, PNG, GIF, BMP, WebP
- **💾 Easy Download**: One-click download of processed images
- **🔒 Privacy First**: All processing happens locally - no data sent to external servers
- **📦 Single File**: Entire application in one Python file for easy deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-background-remover.git
   cd ai-background-remover

Install dependencies
bashpip install flask rembg pillow

Run the application
bashpython app.py

Open your browser
Navigate to http://127.0.0.1:5000

That's it! Start removing backgrounds instantly.

🛠️ Tech Stack

Backend: Python, Flask
AI/ML: rembg (RemBG), PIL/Pillow
Frontend: HTML5, CSS3, JavaScript
UI/UX: Responsive design with modern animations

📱 How It Works

Upload: Drag and drop an image or click to browse
Process: AI automatically detects and removes the background
Download: Get your professional PNG with transparent background

🎯 Use Cases

E-commerce: Product photography with clean backgrounds
Social Media: Profile pictures and content creation
Design: Quick background removal for graphic design projects
Photography: Professional headshots and portraits
Marketing: Clean product images for presentations

🔧 Configuration

The application includes several configurable options:
File Size Limit: 16MB (configurable)
Supported Formats: JPG, PNG, GIF, BMP, WebP
Processing Models: Uses rembg's default U2Net model
Temporary Storage: Auto-cleanup of processed files
