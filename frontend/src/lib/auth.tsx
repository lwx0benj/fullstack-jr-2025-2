export type StoredAuth = {
    access_token: string;
    token_type: string; // "bearer"
    expires_at: number;
};

const LS_KEY = "auth_token";

export function saveAuthToken(params: {
    access_token: string;
    token_type?: string;
    expires_in: number;
}) {
    const { access_token, token_type = "bearer", expires_in } = params;
    const expires_at = Date.now() + Math.max(0, (expires_in - 30) * 1000);

    const toStore: StoredAuth = { access_token, token_type, expires_at };
    localStorage.setItem(LS_KEY, JSON.stringify(toStore));
}

export function readAuthToken(): StoredAuth | null {
    const raw = typeof window !== "undefined" ? localStorage.getItem(LS_KEY) : null;
    if (!raw) return null;
    try {
        const parsed = JSON.parse(raw) as StoredAuth;
        return parsed;
    } catch {
        return null;
    }
}

export function isAuthExpired(auth: StoredAuth | null): boolean {
    if (!auth) return true;
    return Date.now() >= auth.expires_at;
}

export function getAuthHeader(): Record<string, string> | null {
    const auth = readAuthToken();
    if (!auth || isAuthExpired(auth)) return null;

    const scheme = auth.token_type ? auth.token_type : "bearer";
    return { Authorization: `${scheme.charAt(0).toUpperCase() + scheme.slice(1)} ${auth.access_token}` };
}

export function clearAuthToken() {
    localStorage.removeItem(LS_KEY);
}
