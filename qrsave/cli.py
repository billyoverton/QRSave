import click
import qrcode
@click.command()
@click.option('--qrversion', type=click.IntRange(1, 40), default=10, help='QR Version to use for the generated images. 1-40')
@click.option('--errorlevel', type=click.Choice(['L', 'M', 'Q', 'H']), default='L', help='QR Error Level')
@click.option('--prefix', default='qr', help='Prefix to append in front of the file name')
@click.argument('input', type=click.File('rb'))
def qrsave(qrversion, errorlevel, prefix, input):
    errorLevels = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }

    # Determine max data per code by the rsBlocks
    rsBlocks = qrcode.base.rs_blocks(qrversion, errorLevels[errorlevel])
    maxDataCountPerCode = 0
    for i in range(len(rsBlocks)):
        maxDataCountPerCode += rsBlocks[i].data_count
    maxDataCountPerCode -= 3


    qr = qrcode.QRCode(
        version=qrversion,
        error_correction=errorLevels[errorlevel]
    )


    i = 1
    while True:
        chunk = input.read(maxDataCountPerCode)
        if not chunk:
            break

        qr.add_data(chunk)
        im = qr.make_image()
        im.save(prefix + str(i) + ".png")
        qr.clear()

        i = i+1

if __name__ == '__main__':
    qrsave()
