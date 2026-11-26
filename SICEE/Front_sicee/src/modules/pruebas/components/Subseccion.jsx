export default function Subseccion({titulo, children}){
    return(
        <div>
            <h3 className="mb-3 text-sm font-semibold text-[#0f6b4f]">{titulo}</h3>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{children}</div>
        </div>
    )
}

