import { readAuthToken, clearAuthToken} from "@/lib/auth"

export async function infoUser() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    try {
        const storedAuth = await readAuthToken();

        if (!storedAuth || !storedAuth.access_token) {
            throw new Error("Token de autenticação não encontrado.");
        }

        const response = await fetch(`${apiUrl}/api/auth/userinfo`, {
            method: "GET",
            headers: {
                "Authorization": `${storedAuth.token_type} ${storedAuth.access_token}`,
                "Content-Type": "application/json",
            },
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error(`Erro ao buscar informações do usuário: ${response.status}`);
        }

        const userData = await response.json();
        return userData;
    } catch (error) {
        console.error("Erro em userInfor():", error);
        return null;
    }
}

export async function logoutUser() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    try {
        const storedAuth = await readAuthToken();

        if (!storedAuth || !storedAuth.access_token) {
            throw new Error("Token de autenticação não encontrado.");
        }

        const response = await fetch(`${apiUrl}/api/auth/logout`, {
            method: "POST",
            headers: {
                "Authorization": `${storedAuth.token_type} ${storedAuth.access_token}`,
                "Content-Type": "application/json",
            },
            cache: "no-store",
        });

        if (!response.ok) {
            throw new Error(`Erro ao realizar logout: ${response.status}`);
        }

        await clearAuthToken();

        return true;
    } catch (error) {
        console.error("Erro em logoutUser():", error);
        return false;
    }
}




