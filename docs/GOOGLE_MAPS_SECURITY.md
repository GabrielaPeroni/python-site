# Google Maps API Security Guide

This document outlines the security measures implemented to protect against API abuse and unexpected billing charges.

## 1. Rate Limiting (Already Implemented)

We use `django-ratelimit` to limit the number of place submissions:

- **Place Creation**: Limited to **5 submissions per hour per user**
- **Place Updates**: Limited to **10 updates per hour per user**

These limits prevent automated abuse while allowing legitimate users to create and edit places normally.

### How it Works

When a user exceeds the rate limit, they receive a friendly error message and are redirected to the explore page. The limits are tracked per authenticated user using Django's default cache.

### Configuration

Rate limiting can be disabled or adjusted in `.env`:

```env
RATELIMIT_ENABLE=true  # Set to false to disable
```

### Cache Backend

**Development**: Uses in-memory cache (LocMemCache) - works for single-process development servers.

**Production**: For multi-process deployments (Gunicorn, uWSGI), you should use Redis or Memcached:

1. Install Redis:

   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server

   # macOS
   brew install redis
   ```

2. Install Python Redis client:

   ```bash
   poetry add django-redis
   ```

3. Update `config/settings.py`:
   ```python
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/1",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       }
   }
   ```

---

## 2. HTTP Referrer Restrictions (REQUIRED - Manual Setup)

**IMPORTANT**: You must configure HTTP referrer restrictions in Google Cloud Console to prevent unauthorized domains from using your API key.

### Step-by-Step Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to: **APIs & Services** → **Credentials**
4. Click on your API key (the one used in this project)
5. Under **Application restrictions**, select **HTTP referrers (web sites)**
6. Add the following referrers:

   **For Development:**

   ```
   http://localhost/*
   http://127.0.0.1/*
   ```

   **For Production:**

   ```
   https://maricacity.com/*
   https://www.maricacity.com/*
   ```

7. Click **Save**

### Why This Matters

Without referrer restrictions, anyone who finds your API key (visible in page source) could use it on their own website, potentially generating charges on your account.

---

## 3. API Key Restrictions (REQUIRED - Manual Setup)

### Restrict to Specific APIs

1. In the same API key settings page
2. Under **API restrictions**, select **Restrict key**
3. Enable ONLY these APIs:

   - **Maps JavaScript API**
   - **Places API**
   - **Geocoding API**

4. Click **Save**

### Why This Matters

This prevents the key from being used for other Google services, limiting potential abuse.

---

## 4. Daily Budget Alerts (RECOMMENDED)

Set up billing alerts to get notified before charges become significant.

### Step-by-Step Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to: **Billing** → **Budgets & alerts**
3. Click **Create Budget**
4. Configure:

   - **Name**: "MaricaCity Maps API Budget"
   - **Projects**: Select your project
   - **Budget amount**: Set monthly budget (e.g., R$50 or $10 USD)
   - **Threshold rules**: Add alerts at 50%, 75%, 90%, and 100%
   - **Email notifications**: Add your email

5. Click **Save**

### Recommended Budget

For a small community site like MaricaCity with low traffic:

- **Development**: R$10/month (~$2 USD)
- **Production**: R$50/month (~$10 USD)

Google provides $200 monthly credit for Maps Platform, which should cover typical usage.

---

## 5. Usage Monitoring

### Check Current Usage

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to: **APIs & Services** → **Dashboard**
3. Select **Maps JavaScript API**, **Places API**, and **Geocoding API**
4. Review the usage charts

### What to Monitor

- **Daily requests**: Should stay under 1000/day for small sites
- **Spike detection**: Sudden increases may indicate abuse
- **Cost estimates**: Check estimated monthly costs

---

## 6. Additional Django Security

### Environment Variables

The API key is stored in `.env` and never committed to git:

```env
GOOGLE_MAPS_API_KEY=your_key_here
```

### Template Context

The API key is only passed to templates that need it (place forms).

---

## 7. Emergency Response

### If You Suspect Abuse

1. **Disable the API key immediately**:

   - Go to Google Cloud Console → Credentials
   - Click on your API key
   - Click **Disable**

2. **Create a new API key**:

   - Follow the setup steps again
   - Update `.env` with new key
   - Restart Django server

3. **Review billing**:
   - Check for unexpected charges
   - Contact Google Cloud Support if needed

---

## 8. Cost Optimization

### How the APIs Are Charged

- **Maps JavaScript API**: Free up to 28,000 loads/month
- **Places API (Autocomplete)**: Free up to 2,800 requests/month
- **Geocoding API**: Free up to 28,000 requests/month

With $200 monthly credit, you get significantly more.

### Usage Estimation

For a site with 100 active users creating 5 places per month:

- **500 autocomplete sessions**: Well under free tier
- **500 geocoding requests**: Well under free tier
- **1000 map loads** (detail pages): Well under free tier

**Estimated cost**: $0/month (within free tier)

---

## 9. Testing Security Measures

### Test Rate Limiting

1. Log in as a regular user
2. Try creating 6 places within one hour
3. The 6th attempt should be blocked with a friendly error message

### Test Referrer Restrictions

1. After setting up referrer restrictions
2. Try loading your site from the allowed domains (localhost, production)
3. The map should work normally
4. If someone tries using your key on a different domain, it will fail

---

## 10. Summary Checklist

- [x] **Rate limiting implemented** (5 creates/hour, 10 updates/hour)
- [ ] **HTTP referrer restrictions configured** in Google Cloud Console
- [ ] **API restrictions configured** (only Maps, Places, Geocoding)
- [ ] **Daily budget alerts set up** in Google Cloud Console
- [ ] **Tested rate limiting** by exceeding limits
- [ ] **Monitoring dashboard bookmarked** for regular checks

---

## Support

If you encounter issues:

1. Check Google Cloud Console logs
2. Review Django error logs
3. Verify API key restrictions
4. Contact Google Cloud Support for billing questions

---

**Last Updated**: 2025-10-21
