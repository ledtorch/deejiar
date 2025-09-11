#!/bin/sh

# ci_post_clone.sh
# Place this in your root repository directory

set -e

echo "🚀 Starting Deejiar build process..."

# Navigate to the capacitor-ios directory
cd capacitor-ios

# Install dependencies using Yarn (since you're using Yarn 4.9.2)
echo "📦 Installing dependencies..."
yarn install --frozen-lockfile

# Build the Vue.js app
echo "🔨 Building Vue app..."
yarn build

# Sync Capacitor (this updates the iOS native project)
echo "🔄 Syncing Capacitor..."
npx cap sync ios

echo "✅ Build preparation completed!"