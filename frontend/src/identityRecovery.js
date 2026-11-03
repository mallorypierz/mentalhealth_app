// Recover only a rejected browser credential; never delete saved data or retry writes.
export async function restoreIdentity(request, getAccess, clearAccess) {
  if (getAccess()?.access_token) {
    try { return await request('/identity'); }
    catch (error) {
      if (error.status !== 401) throw error;
      clearAccess();
    }
  }
  return request('/identity/bootstrap', 'POST', { bootstrap_id: crypto.randomUUID() });
}
