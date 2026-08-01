export default function PageHeader({

    title,

    subtitle

}){

    return(

        <div
            style={{

                marginBottom:"25px"

            }}
        >

            <h1>{title}</h1>

            <p
                style={{

                    color:"#666"

                }}
            >
                {subtitle}
            </p>

        </div>

    );

}
