$(function(){
    refreshInvoices()
    
	$('#fetch-button').click(function() {
        refreshInvoices()
	})
})

function refreshInvoices(){
    $.ajax({
        url: '/invoice/view',
        type: 'POST',
        success: function(response) {
            if( response['status'] != 200 ){
                console.log(response['message'])
                return
            }
            
            payload = JSON.parse(response['payload'])
            invoices = payload['invoices']
        
            invoiceHTMLs = []
            for (const [id, invoice] of Object.entries(invoices)) {
                invoiceHTMLs.push(createInvoiceHTML(id, invoice))
            }
            
            $("#invoice-list").empty();
            for( i = 0; i < invoiceHTMLs.length; i++ ){
                $('#invoice-list')
                .append(invoiceHTMLs[i])
            }
        }
    })
}

function createInvoiceHTML(id, invoice){
    header = $('<h3>').html('Invoice ID: '  + id)
    
    localDate = new Date(invoice['invoice']['date'])
    year = localDate.getFullYear()
    month = localDate.getMonth() + 1  // + 1 for 0 base offset
    day = localDate.getDate()
    dateString = year + '-' + month + '-' + day
    date = $('<h3>').html('Invoice Date: ' + dateString)
    
    invoiceDivs = createInvoiceItems(invoice['items'])
    invoiceItemList = 
        $('<div>')
        .addClass('grid-3')
    for( i = 0; i < invoiceDivs.length; i++ ){
        invoiceItemList.append(invoiceDivs[i])
    }
    
    return $('<div>')
    .addClass('flex-column small-box light-mid-bg margin-half')
    .append(
        $('<div>').addClass('flex-column center invoice-information')
        .append(header)
        .append(date)
        .append($('<h3>').html('Invoice Items')
            .addClass('text-no-wrap')))
    .append(invoiceItemList)
}


function submitCreateInvoice(){
    data = {}
	$('#invoice-form').serializeArray().map( function(x){ data[x.name] = x.value }) 
    if (data['date'] == ''){
        delete data['date']
    } else{
        date = new Date(data['date'])
        UTCseconds = (date.getTime() + date.getTimezoneOffset() * 60 * 1000) / 1000; //convert to UTC seconds since epoch.
        data['date'] = UTCseconds 
    }
    
    $.ajax({
        url: '/invoice/create',
        type: 'POST',
        data: JSON.stringify(data),
        success: function(response) {
            if( response['status'] != 200 ){
                console.log(response)
                return
            }
            alert("Created Invoice!")
            refreshInvoices()
        }
    })
    return false
}

function createInvoiceItems(items){
    itemDivs = []
    for(i = 0; i < items.length; i++){
        itemDivs.push(
            createInvoiceItemDiv(items[i]))
    }
    return itemDivs
}

function createInvoiceItemDiv(item){ 
    return $('<div>')
        .addClass('flex-column margin-half')
        .append($('<div>').html( "ID: "+ item['id']))
        .append($('<div>').html( "Description: "+ item['description'] ))
        .append($('<div>').html( "Units: "+ item['units'] ))
        .append($('<div>').html( "Amount: "+ item['amount'] ))
}