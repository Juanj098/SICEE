export default function Seccion({titulo, descripcion, children}){

    return (
        <section className="rounded-xl bg-white p-6 sm:p-7">
            <h2 className="text-lg font-semibold tracking-toght"> {titulo} </h2>
            {descripcion && <p  className="mt-1 text-sm text-[#5d6862]">{descripcion}</p>}
            <div className="mt-5">
                {children}
            </div>
        </section>
    )
}
