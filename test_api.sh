#!/bin/bash
TOKEN="eyJpZCI6MTQsImVtYWlsIjoidmJvc3NvdTI3MCBnbWFpbC5jb20iLCJleHAiOjE3OTUwMzY4MTQ1ODN9.bc41c2201f3ff3f964acf6d42d03a660f3d350d4e9eed66813dc3acdb0c955d1"
echo "🧪 Test GET /api/memories"
curl -s http://localhost:8080/api/memories -H "Authorization: Bearer $TOKEN"
echo ""
