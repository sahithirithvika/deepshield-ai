# ✅ DeepShield AI - Testing Checklist

## Pre-Deployment Testing (Local)

### 1. Environment Setup
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `certificates/` folder exists (auto-created)
- [ ] `data/` folder exists with `ledger.json`

### 2. Run Local Server
```bash
streamlit run app.py
```
- [ ] Server starts without errors
- [ ] Opens at `http://localhost:8501`
- [ ] UI loads correctly with glassmorphism design

### 3. Image Upload Testing
- [ ] Upload JPG image (< 200MB)
- [ ] Upload PNG image (< 200MB)
- [ ] Image displays correctly
- [ ] Analysis completes in < 5 seconds
- [ ] Authenticity score displayed
- [ ] AI Detection score displayed
- [ ] Piracy risk level shown
- [ ] Verdict displayed (Real/Suspicious/Fake)
- [ ] Certificate generated
- [ ] PDF download works

### 4. Video Upload Testing
- [ ] Upload MP4 video (< 200MB)
- [ ] Upload MOV video (< 200MB)
- [ ] Video plays correctly
- [ ] Frame extraction works
- [ ] Video authenticity score displayed
- [ ] Audio integrity score displayed
- [ ] AI Detection score displayed
- [ ] Temporal consistency checked
- [ ] Certificate generated
- [ ] PDF download works

### 5. Detection Accuracy Testing

**Test with Real Content:**
- [ ] Real sports photo → Should show "Real" (>82%)
- [ ] Real sports video → Should show "Real" (>82%)
- [ ] Scores should be consistent (difference < 15%)

**Test with AI-Generated Content:**
- [ ] AI-generated image → Should show "Fake" (<68%)
- [ ] AI-generated video → Should show "Fake" (<68%)
- [ ] Detection confidence should be high

**Test with Suspicious Content:**
- [ ] Heavily edited image → Should show "Suspicious" (68-82%)
- [ ] Low-quality video → May show "Suspicious"

### 6. UI/UX Testing
- [ ] Glassmorphism effects visible
- [ ] Animations smooth
- [ ] Hover effects work
- [ ] Progress bar animates
- [ ] Metric boxes display correctly
- [ ] Expander works
- [ ] Download button styled correctly
- [ ] Mobile responsive (test on phone)

### 7. Certificate Testing
- [ ] Certificate ID generated (UUID format)
- [ ] Timestamp correct
- [ ] Verdict matches analysis
- [ ] Score matches analysis
- [ ] PDF opens correctly
- [ ] PDF contains all information
- [ ] Blockchain hash displayed
- [ ] Entry added to `data/ledger.json`

---

## Post-Deployment Testing (Cloud Run)

### 1. Deployment Verification
- [ ] Deployment completed without errors
- [ ] Service URL received
- [ ] URL is accessible
- [ ] HTTPS enabled (automatic)

### 2. Cloud Functionality Testing
```bash
# Get service URL
gcloud run services describe deepshield-ai --region asia-south1 --format 'value(status.url)'
```

- [ ] Open URL in browser
- [ ] App loads correctly
- [ ] Background image loads
- [ ] All UI elements visible
- [ ] No console errors (F12 → Console)

### 3. Upload Testing (Cloud)
- [ ] Upload image from desktop
- [ ] Upload video from desktop
- [ ] Analysis completes successfully
- [ ] Results display correctly
- [ ] Certificate downloads
- [ ] PDF opens correctly

### 4. Performance Testing
- [ ] Cold start time < 30 seconds
- [ ] Warm request time < 5 seconds
- [ ] Analysis time < 10 seconds
- [ ] No timeout errors
- [ ] No memory errors

### 5. Multi-User Testing
- [ ] Open URL in multiple browsers
- [ ] Upload different files simultaneously
- [ ] All requests complete successfully
- [ ] No conflicts or errors

### 6. Error Handling
- [ ] Upload invalid file type → Shows error
- [ ] Upload file > 200MB → Shows error
- [ ] Upload corrupted file → Handles gracefully
- [ ] Network interruption → Shows error message

### 7. Logs Verification
```bash
# Check logs
gcloud run logs read deepshield-ai --limit 50
```

- [ ] No error messages
- [ ] Requests logged correctly
- [ ] Analysis steps logged
- [ ] Certificate generation logged

---

## Security Testing

### 1. Access Control
- [ ] Public access works (unauthenticated)
- [ ] HTTPS enforced
- [ ] No sensitive data exposed in logs
- [ ] No API keys in client-side code

### 2. Input Validation
- [ ] File type validation works
- [ ] File size validation works
- [ ] Malicious file upload handled
- [ ] XSS protection enabled

### 3. Data Privacy
- [ ] Uploaded files not stored permanently
- [ ] Certificates stored securely
- [ ] Ledger data encrypted
- [ ] No PII collected

---

## Performance Benchmarks

### Expected Metrics
- **Image Analysis**: 2-4 seconds
- **Video Analysis**: 5-15 seconds (depending on length)
- **Certificate Generation**: < 1 second
- **PDF Download**: < 1 second
- **Cold Start**: 10-30 seconds
- **Warm Request**: < 3 seconds

### Load Testing
```bash
# Test with multiple concurrent requests
for i in {1..10}; do
  curl -X POST [YOUR_URL] &
done
```

- [ ] Handles 10 concurrent requests
- [ ] No timeout errors
- [ ] Response time < 10 seconds
- [ ] Auto-scaling works

---

## Browser Compatibility

### Desktop Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Mobile Browsers
- [ ] Chrome Mobile
- [ ] Safari iOS
- [ ] Samsung Internet

---

## Hackathon Submission Checklist

### Required Links
- [ ] MVP Link copied
- [ ] Working Prototype Link copied
- [ ] Both links are the same (Cloud Run URL)
- [ ] Links are publicly accessible
- [ ] Links work in incognito mode

### Demo Preparation
- [ ] Test images/videos ready
- [ ] Demo script prepared
- [ ] Key features highlighted
- [ ] Performance metrics noted
- [ ] Screenshots/recordings captured

### Documentation
- [ ] README.md complete
- [ ] DEPLOYMENT.md available
- [ ] QUICKSTART.md available
- [ ] Code comments added
- [ ] Architecture documented

### Repository
- [ ] All code committed
- [ ] Git history clean
- [ ] No sensitive data in repo
- [ ] .gitignore configured
- [ ] LICENSE file present

---

## Troubleshooting Guide

### Issue: App Won't Start Locally
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for port conflicts
lsof -i :8501
```

### Issue: Certificate Generation Fails
```bash
# Check certificates folder exists
ls -la certificates/

# Create if missing
mkdir -p certificates
```

### Issue: Deployment Fails
```bash
# Check Docker is running
docker ps

# Check gcloud auth
gcloud auth list

# Check project
gcloud config get-value project
```

### Issue: Analysis Takes Too Long
- Check file size (should be < 200MB)
- Check internet connection
- Check Cloud Run logs for errors
- Increase timeout if needed

### Issue: Certificate Download Fails
- Check browser download settings
- Check popup blocker
- Try different browser
- Check Cloud Run logs

---

## Success Criteria

### Minimum Viable Product (MVP)
- ✅ Upload image/video
- ✅ Analyze content
- ✅ Display results
- ✅ Generate certificate
- ✅ Download PDF

### Full Feature Set
- ✅ Multi-modal detection
- ✅ Real-time analysis
- ✅ Blockchain verification
- ✅ Professional UI
- ✅ Cloud deployment
- ✅ Auto-scaling
- ✅ Error handling
- ✅ Performance optimization

---

## Final Verification

Before submitting to hackathon:

1. **Test the live URL** in incognito mode
2. **Upload test content** and verify results
3. **Download certificate** and verify PDF
4. **Check logs** for any errors
5. **Verify performance** meets benchmarks
6. **Test on mobile** device
7. **Share URL** with team member for testing
8. **Take screenshots** for submission
9. **Record demo video** (optional)
10. **Submit with confidence!** 🚀

---

## Contact for Issues

If you encounter any issues during testing:
- Check logs: `gcloud run logs read deepshield-ai`
- Review DEPLOYMENT.md
- Check QUICKSTART.md
- Verify all prerequisites met

---

**Last Updated**: 2026-04-22

