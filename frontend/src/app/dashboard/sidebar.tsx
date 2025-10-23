"use client";
import { useEffect, useState } from 'react'

import Image from 'next/image'
import { useRouter } from "next/navigation";

import NavButton from './navbutton'
import { infoUser } from './user'

export default function Sidebar() {
    const [user, setUser] = useState<{ name: string } | null>(null)
    const router = useRouter();

    useEffect(() => {
        async function loadUser() {
            const u = await infoUser()
            if (!u) {
                router.push("/login");
                return;
            }
            setUser(u)
        }
        loadUser()
    }, [])

    return (
        <div className="flex h-full flex-col justify-between p-6">
            <div>
                <div className="flex flex-col items-center gap-4 rounded-2xl bg-white/10 p-6">
                    <div className="relative h-24 w-24 overflow-hidden rounded-full ring-4 ring-white/20">
                        <Image src="/avatar-svgrepo-com.svg" alt="Foto de perfil" fill className="object-cover" />
                    </div>
                    <p className="text-center text-sm leading-relaxed text-white/90">
                        Olá, <strong>{user?.name}</strong>! Pronta para organizar o seu dia?
                    </p>
                </div>
                <nav className="mt-6 flex flex-col gap-3">
                    <NavButton icon="user" label="Perfil" active={false} />
                    <NavButton icon="task" label="Tarefas" active={false} />
                </nav>
            </div>
            <button className="mt-6 w-full rounded-xl bg-white/20 px-4 py-3 text-center text-base font-medium text-white hover:bg-white/25 focus:outline-none">
                Sair
            </button>
        </div>
    )
}
