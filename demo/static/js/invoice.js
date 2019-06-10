$(function(){
    $.ajax({
        url: '/invoice/view',
        type: 'POST',
        success: function(response) {
            if( response['status'] != 200 ){
                return
            }
            
            payload = JSON.parse(response['payload'])
            invoices = payload['invoices']
            
            invoiceHTMLs = []
            for (const [id, invoice] of Object.entries(invoices)) {
                invoiceHTMLs.push(createInvoiceHTML(id, invoice))
            }
            
            for( i = 0; i < invoiceHTMLs.length; i++ ){
                $('#invoice-list')
                .append(invoiceHTMLs[i])
            }
        }
    })
    
	$('#fetch-button').click(function() {
        $.ajax({
            url: '/invoice/view',
            type: 'POST',
            success: function(response) {
                if( response['status'] != 200 ){
                    return
                }
                
                payload = JSON.parse(response['payload'])
                invoices = payload['invoices']
                
                invoiceHTMLs = []
                for (const [id, invoice] of Object.entries(invoices)) {
                    invoiceHTMLs.push(createInvoiceHTML(id, invoice))
                }
                
                for( i = 0; i < invoiceHTMLs.length; i++ ){
                    $('#invoice-list')
                    .append(invoiceHTMLs[i])
                }
            }
        })
	})
})

function createInvoiceHTML(id, invoice){
    header = $('<h3>').html('Invoice ID: '  + id)
    
    localDate = new Date(invoice['invoice']['date'])
    year = localDate.getFullYear()
    month = localDate.getMonth()
    day = localDate.getDate()
    dateString = year + '-' + month + '-' + day
    date = $('<h3>').html('Invoice Date: ' + dateString)
    
    if( invoice['items'].length <= 0 ){
        return $('<div>')
        .addClass('flex-column small-box light-mid-bg margin-half ')
        .append(header)
        .append(date)
    }
    
    invoiceDivs = createInvoiceItems(invoice['items'])
    invoiceItemList = 
        $('<div>')
        .addClass('flex flex-wrap')
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