import { NextResponse } from 'next/server';

interface SearchRequest {
  query: string;
}

export async function POST(request: Request) {
  try {
    const body: SearchRequest = await request.json();

    // Call the Python microservice
    const response = await fetch('https://5000-01jee5pr9xb2j262zxr99q70r6.cloudspaces.litng.ai/search', {  // Update the URL to match your Flask app's URL
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: body.query }),
    });

    if (!response.ok) {
      console.error('Failed to fetch search results:', response.statusText);
      return NextResponse.json({ error: 'Failed to fetch search results' }, { status: response.status });
    }

    const results = await response.json();
    return NextResponse.json(results);
  } catch (error) {
    console.error('Error in POST request:', error);
    return NextResponse.json({ error: 'An error occurred while fetching search results' }, { status: 500 });
  }
}