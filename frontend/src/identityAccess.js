const KEY = 'coursework-browser-identity';
let access;
try { access = JSON.parse(sessionStorage.getItem(KEY) || 'null'); } catch { access = null; }
export const getAccess = () => access;
export function setAccess(value) {
  sessionStorage.setItem(KEY, JSON.stringify(value));
  access = value;
}
export const ownerKey = () => getAccess()?.active_owner_id || 'legacy';
