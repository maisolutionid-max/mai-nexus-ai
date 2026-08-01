import MainLayout from "../layouts/MainLayout";
import PageHeader from "../components/PageHeader";
import DataTable from "../components/DataTable";

export default function Customer(){

const columns=[
"ID",
"Nama",
"Email",
"Telepon"
];

const data=[
["1","PT ABC","abc@mail.com","08123456789"],
["2","PT XYZ","xyz@mail.com","08129876543"],
];

return(

<MainLayout>

<PageHeader

title="Customer"

subtitle="Customer Management"

/>

<DataTable

columns={columns}

data={data}

/>

</MainLayout>

);

}
