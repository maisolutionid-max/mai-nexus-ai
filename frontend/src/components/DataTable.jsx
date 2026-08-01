export default function DataTable({

    columns,

    data

}){

    return(

        <table
            style={{

                width:"100%",

                borderCollapse:"collapse",

                background:"#fff"

            }}
        >

            <thead>

                <tr>

                    {

                        columns.map((col)=>(

                            <th
                                key={col}

                                style={{

                                    padding:"15px",

                                    borderBottom:"1px solid #ddd",

                                    textAlign:"left"

                                }}
                            >

                                {col}

                            </th>

                        ))

                    }

                </tr>

            </thead>

            <tbody>

                {

                    data.map((row,index)=>(

                        <tr key={index}>

                            {

                                row.map((cell,i)=>(

                                    <td

                                        key={i}

                                        style={{

                                            padding:"15px",

                                            borderBottom:"1px solid #eee"

                                        }}

                                    >

                                        {cell}

                                    </td>

                                ))

                            }

                        </tr>

                    ))

                }

            </tbody>

        </table>

    );

}
