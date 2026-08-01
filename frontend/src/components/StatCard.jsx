export default function StatCard({

    title,

    value,

    color = "#2563eb"

}){

    return(

        <div
            style={{

                background:"#fff",

                borderRadius:"12px",

                padding:"20px",

                borderLeft:`6px solid ${color}`,

                boxShadow:"0 2px 10px rgba(0,0,0,.08)"

            }}
        >

            <h3>{title}</h3>

            <h1
                style={{

                    color,

                    marginTop:"15px"

                }}
            >
                {value}
            </h1>

        </div>

    );

}
