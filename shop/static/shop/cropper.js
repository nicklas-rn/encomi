var image_workspaceSpan = document.querySelector('.image-workspace span')
var actionButton = document.querySelectorAll('.action-button button')
var hiddenUpload = document.querySelector('.action-button .hidden-upload')
var image_workspace = document.querySelector('.image-workspace img')
var options
var cropper


// upload image
actionButton[0].onclick = () => hiddenUpload.click()
hiddenUpload.onchange = () => {
    // apdate on new file selected issue removed here
    document.querySelector('.image-workspace').innerHTML = `<img src="" alt="">`
    image_workspace = document.querySelector('.image-workspace img')

    var file = hiddenUpload.files[0]
    var url = window.URL.createObjectURL(new Blob([file], { type : 'image/jpg' }))
    console.log(url)
    image_workspace.src = url
    image_workspaceSpan.style.display = 'none'

    options = {
        dragMode: 'move',
        preview: '.img-preview',
        viewMode: 2,
        modal: false,
        aspectRatio: 380/470,
        background: false,
        ready: function(){
            // download cropped image
            actionButton[1].onclick = () => {
                cropper.getCroppedCanvas().toBlob((blob) => {
                    var downloadUrl = window.URL.createObjectURL(blob)

                    /*
                    var a = document.createElement('a')
                    a.href = downloadUrl
                    a.download = 'cropped-image.jpg' // output image name
                    a.click()
                    actionButton[1].innerText = 'Download'*/

                    let imgFile = new File([blob], "img.jpg",{type:"image/jpeg", lastModified:new Date().getTime()});
                    let fileContainer = new DataTransfer();
                    fileContainer.items.add(imgFile);

                    console.log(blob)
                    setImage(downloadUrl, fileContainer)
                    closeCropper()
                })
            }
        }
    }

    cropper = new Cropper(image_workspace, options)
}