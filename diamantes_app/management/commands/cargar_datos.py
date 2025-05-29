from django.core.management.base import BaseCommand
from diamantes_app.models import Diamond
import csv

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Iniciando carga...")  # Confirma inicio del proceso
        try:
            with open('Diamonds_citt.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                total = 0
                for i, row in enumerate(reader):
                    try:
                        Diamond.objects.create(
                            carat=row['carat'],
                            cut=row['cut'],
                            color=row['color'],
                            clarity=row['clarity'],
                            depth=row['depth'],
                            table=row['table'],
                            price=row['price'],
                            x=row['x'],
                            y=row['y'],
                            z=row['z']
                        )
                        total += 1
                        if total % 1000 == 0:
                            print(f"{total} registros insertados...")
                    except Exception as e:
                        print(f"❌ Error en la fila {i+1}: {e}")
                self.stdout.write(self.style.SUCCESS(f"✅ {total} registros cargados correctamente."))
                print("Finalizó carga")  # Confirma fin del proceso
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("❌ Archivo 'Diamonds_citt.csv' no encontrado. Asegúrate de que esté en la raíz del proyecto."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error general al cargar datos: {e}"))
