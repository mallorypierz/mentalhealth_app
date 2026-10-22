export async function api(path, method = 'GET', body) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  try {
    const response = await fetch(`/api${path}`, {
      method, signal: controller.signal,
      headers: body ? { 'Content-Type': 'application/json' } : {},
      body: body ? JSON.stringify(body) : undefined,
    });
    const result = await response.json();
    if (!response.ok) {
      const error = new Error(result.error?.message || 'Request failed.');
      error.status = response.status; error.persistence = result.persistence;
      throw error;
    }
    return result;
  } catch (error) {
    if (!error.status) error.persistence = 'unknown';
    throw error;
  } finally { clearTimeout(timeout); }
}
