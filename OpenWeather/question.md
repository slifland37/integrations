# Weather API Consistency Bug - Interview Question

## Background

You're working on a weather service that fetches current weather data for various cities using the Weatherstack API. The service is used by thousands of users daily, and **consistency is critical** - users expect the same city to be returned for the same input, regardless of how they type the city name.

While we rely on the Weatherstack API to infer the correct city from user input, it's essential that our application provides consistent results. The specific city returned doesn't matter as much as ensuring that identical queries always return the same result.

## The Problem

A test is failing in our weather service. Here's what we know:

### Test Details
You can run the tests using:
```
python3 -m pytest test_weather.py -v
```

### API Behavior Investigation

When we test the API directly, we see Kolno Poland. Try it out!

**Query 1**: `curl "http://api.weatherstack.com/current?access_key=47a6f99543add63c6bcd82ec6ea8f6b1&query=Koln"`
```json
{
  "location": {
    "name": "Kolno",
    "country": "Poland"
  },
  "current": {
    "temperature": 12,
    "weather_descriptions": ["Cloudy"]
  }
}
```

## Your Task

1. **Identify the root cause**: Why is the test failing?

2. **Propose a solution**: How would you fix this issue to ensure consistent results?

3. **Consider edge cases**: What other similar issues might exist in the codebase?


**Question**: What's causing the test failure, and how would you fix the code?