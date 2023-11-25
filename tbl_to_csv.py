from pathlib import Path
import gzip
import csv


TPCH_ROOT = Path.home() / "Downloads" / "tpch100"
OUT_DIR = TPCH_ROOT / "split"
OUT_DIR.mkdir(exist_ok=True)

writers = {}
locks = {}

def process_row(row):
   sd = row[10]
   if not sd:
      print("weird row", row)
      return
   if sd not in writers:
      try:
         writer = csv.writer(open(OUT_DIR / f"{sd}.csv", "wt"))
      except OSError:
         print(len(writers))
         raise
      writers[sd] = writer
      # locks[sd] = Lock()
   else:
      writer = writers[sd]
   # with locks[sd]:
   writer.writerow(row)


def process_file(file: Path):
   print(file)
   with gzip.open(file, mode="rt") as f:
      r = csv.reader(f, delimiter="|")
      # outs = defaultdict(list)
      for row in r:
          process_row(row)

# with ThreadPoolExecutor() as pool:
for file in sorted(TPCH_ROOT.iterdir()):
   if file.suffix != ".gz":
      continue
   process_file(file)
