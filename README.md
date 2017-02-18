# auto-injector

I creted this to quickly rename the injects received during the Collegiate
Cyber Defence Competition based on the inject number and name listed in the PDF
file.


## Usage

```sh
./auto-injector 'path/with/glob/to/*.pdf'
```


## Dependencies

- Python 3.5
- `pdftotext`: This is included in many Linux distros. You can find it in
  poppler-utils, or the Windows port of Xpdf.


## Future

- Support custom output file names
- Support cutom `pdftotext` invocation
