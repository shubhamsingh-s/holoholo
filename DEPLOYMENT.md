# Deploying Holoholo to Railway

This guide will help you deploy your Holoholo e-commerce website to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your Holoholo project pushed to GitHub

## Step 1: Prepare Your Project

Your project is already configured for Railway deployment with the following files:
- `Procfile` - Tells Railway how to run your app
- `requirements.txt` - Lists Python dependencies
- `runtime.txt` - Specifies Python version

## Step 2: Deploy to Railway

### Option 1: Deploy from GitHub (Recommended)

1. **Connect Railway to GitHub:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `holoholo` repository

2. **Configure Environment Variables:**
   - In your Railway project dashboard, go to "Variables" tab
   - Add the following environment variables:
     ```
     SECRET_KEY=your-super-secret-key-here
     FLASK_ENV=production
     ```

3. **Deploy:**
   - Railway will automatically detect your Flask app
   - It will install dependencies from `requirements.txt`
   - Your app will be deployed and get a public URL

### Option 2: Deploy from CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Deploy:**
   ```bash
   railway up
   ```

## Step 3: Configure Database (Optional)

For production, you might want to use a PostgreSQL database:

1. **Add PostgreSQL to your Railway project:**
   - In Railway dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will provide a `DATABASE_URL` environment variable

2. **Update your app to use PostgreSQL:**
   - Add `psycopg2-binary` to your `requirements.txt`
   - Railway will automatically set the `DATABASE_URL` environment variable

## Step 4: Custom Domain (Optional)

1. **Add Custom Domain:**
   - In Railway dashboard, go to "Settings" → "Domains"
   - Add your custom domain
   - Configure DNS records as instructed

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `your-secret-key-here` |
| `DATABASE_URL` | Database connection string | `sqlite:///holoholo.db` |
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Port to run the app on | `5000` (set by Railway) |

## Admin Access

After deployment, you can access the admin panel:
- **URL:** `https://your-app.railway.app/admin`
- **Username:** `admin`
- **Password:** `admin123`

**Important:** Change the admin password after first login!

## Troubleshooting

### Common Issues:

1. **Build Fails:**
   - Check that all dependencies are in `requirements.txt`
   - Ensure `Procfile` is correctly formatted

2. **App Won't Start:**
   - Check Railway logs in the dashboard
   - Verify environment variables are set correctly

3. **Database Issues:**
   - Ensure `DATABASE_URL` is set correctly
   - Check that database is accessible

### Viewing Logs:

```bash
railway logs
```

## Performance Tips

1. **Enable Caching:**
   - Consider adding Redis for session storage
   - Implement static file caching

2. **Database Optimization:**
   - Add database indexes for better performance
   - Consider using connection pooling

3. **Static Files:**
   - Use a CDN for static assets in production
   - Optimize images before upload

## Security Considerations

1. **Change Default Credentials:**
   - Update admin username/password
   - Use strong, unique passwords

2. **Environment Variables:**
   - Never commit sensitive data to Git
   - Use Railway's environment variable system

3. **HTTPS:**
   - Railway provides HTTPS by default
   - Ensure all external links use HTTPS

## Support

If you encounter issues:
1. Check Railway's [documentation](https://docs.railway.app)
2. View your app logs in Railway dashboard
3. Check the [Flask documentation](https://flask.palletsprojects.com/)

Your Holoholo e-commerce website should now be live on Railway! 🚀 