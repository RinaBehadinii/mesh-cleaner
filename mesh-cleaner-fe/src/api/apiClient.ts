export const BASE_URL = process.env.REACT_APP_API_URL!;

export async function postForm<T>(endpoint: string, formData: FormData): Promise<T> {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || res.statusText);
    }

    return res.json();
}

export async function getJson<T>(endpoint: string): Promise<T> {
    const res = await fetch(`${BASE_URL}${endpoint}`);

    if (!res.ok) {
        const errorText = await res.text().catch(() => "");
        throw new Error(errorText || res.statusText);
    }

    return res.json();
}
