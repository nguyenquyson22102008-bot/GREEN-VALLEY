# Vercel Speed Insights Integration

This project has been configured with Vercel Speed Insights to track web performance metrics and Core Web Vitals.

## What Was Added

1. **Package Installation**: `@vercel/speed-insights` package installed via npm
2. **Build Tool**: `esbuild` added as a dev dependency for bundling
3. **Speed Insights Initialization**: Created `js/speed-insights.js` that imports and initializes the Speed Insights library
4. **Bundled Script**: Generated `js/speed-insights.bundle.js` containing the minified Speed Insights code
5. **HTML Integration**: Added the Speed Insights script to all HTML pages:
   - index.html
   - trangchu.html
   - gioithieu.html
   - tinhnang.html
   - loaicay.html
   - dungcu.html
   - lienhe.html

## How It Works

The Speed Insights script is loaded in the `<head>` section of each page with the `defer` attribute, ensuring it loads asynchronously without blocking page rendering. The script automatically:

- Tracks Core Web Vitals (LCP, FID, CLS, etc.)
- Measures page performance metrics
- Sends data to Vercel when deployed on Vercel
- Does NOT track data in development mode (localhost)

## Building

After making changes to `js/speed-insights.js`, rebuild the bundle:

```bash
npm run build
```

This generates the minified `js/speed-insights.bundle.js` file that is loaded by the HTML pages.

## Deployment

When deployed to Vercel:

1. Enable Speed Insights in the Vercel Dashboard for your project
2. Deploy your site normally
3. Performance data will start appearing in the Speed Insights dashboard

The library will automatically detect the Vercel environment and start tracking metrics.

## Development

Speed Insights does not track data in development mode (when running locally). This prevents development activity from skewing your analytics.

## Package.json Scripts

- `npm run build` - Bundles the Speed Insights initialization script
- `npm test` - Currently not configured (placeholder)

## Files Modified

- **package.json**: Added dependencies and build script
- **.gitignore**: Created to exclude node_modules
- **js/speed-insights.js**: Source file for Speed Insights initialization
- **js/speed-insights.bundle.js**: Generated bundle (tracked in git for easy deployment)
- **All HTML files**: Added script tag to load Speed Insights

## Documentation

For more information, see the official Vercel Speed Insights documentation:
https://vercel.com/docs/speed-insights/quickstart
