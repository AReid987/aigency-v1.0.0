import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');

  if (code) {
    const supabase = createRouteHandlerClient({ cookies });
    try {
      await supabase.auth.exchangeCodeForSession(code);
      // Successfully exchanged code for session.
      // You might want to redirect to a specific page after login,
      // e.g., a dashboard or the user's profile.
      // Or, if the user was on a specific page before OAuth,
      // you could try to redirect them back there if you stored that info.
      return NextResponse.redirect(requestUrl.origin + '/'); // Redirect to home page
    } catch (error) {
      console.error('Error exchanging code for session:', error);
      // Handle error, maybe redirect to an error page or login page with an error message
      return NextResponse.redirect(requestUrl.origin + '/login?error=auth_callback_failed');
    }
  } else {
    console.error('No code found in callback URL');
    // Handle missing code, redirect to an error page or login page
    return NextResponse.redirect(requestUrl.origin + '/login?error=no_code_in_callback');
  }
}