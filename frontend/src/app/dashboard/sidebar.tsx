// components/Sidebar.tsx
import Image from 'next/image'
import NavButton from './navbutton'

export default function Sidebar() {
  return (
    <div className="flex h-full flex-col justify-between p-6">
      <div>
        <div className="flex flex-col items-center gap-4 rounded-2xl bg-white/10 p-6">
          <div className="relative h-24 w-24 overflow-hidden rounded-full ring-4 ring-white/20">
            <Image src="/avatar-svgrepo-com.svg" alt="Foto de perfil" fill className="object-cover" />
          </div>
          <p className="text-center text-sm leading-relaxed text-white/90">
            Olá, Carla! Pronta para organizar o seu dia?
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
