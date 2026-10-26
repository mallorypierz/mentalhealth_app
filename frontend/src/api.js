import { getAccess } from './identityAccess.js';
export async function api(path, method = 'GET', body) {
  const access = getAccess();
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  try {
    const response = await fetch(`/api${path}`, {
      method, signal: controller.signal,
      headers: { ...(body ? { 'Content-Type': 'application/json' } : {}), ...(access?.access_token ? { Authorization: `Bearer ${access.access_token}`, 'X-Context-Version': String(access.context_version) } : {}) },
      body: body ? JSON.stringify(body) : undefined,
    });
    const result = await response.json();
    if (getAccess() !== access) throw new Error('Profile changed. This response was ignored.');
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
