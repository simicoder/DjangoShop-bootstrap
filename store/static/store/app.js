function PreviewImage()
    {
        let imgid = event.srcElement.id.substring(8,9);
        let oFReader = new FileReader();
        oFReader.readAsDataURL(document.getElementById(event.srcElement.id).files[0]);

        oFReader.onload = function (oFREvent) {
            document.getElementById(imgid).src = oFREvent.target.result;
        }
    };