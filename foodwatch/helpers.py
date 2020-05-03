import json
import zlib
from win10toast import ToastNotifier


class Helpers:

    @staticmethod
    def firetoast(value: int, pcount: int) -> None:
        place = ['Cuatro Caminos', 'Carlos Tercero',  '5tay42']
        toaster = ToastNotifier()

        print("%s productos encontrados" % str(pcount))
        toaster.show_toast(
            "Productos encontrados en " + place[value],
            "%s productos encontrados" % str(pcount),
            duration=30
        )

    @staticmethod
    def mkhash(pname: str, pprice: str) -> str:
        """
        Create a deterministic hash from product name and price
        """
        strenc = (pname+pprice).encode()
        return str(zlib.adler32(strenc))

    @staticmethod
    def ispresent(phash: str) -> bool:
        """
         Check if a product hash is present in the data.jl
        """
        with open('data.jl') as file:
            for line in file:
                if json.loads(line).get("chk") == phash:
                    return True

        return False
