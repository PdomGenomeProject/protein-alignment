# Reference protein alignment

This data set is part of the [*Polistes dominula* genome project][pdomproj], and provides details regarding the alignment of reference proteins to the *P. dominula* genome, as described in (Standage *et al.*, manuscript in preparation).
Included in this data set are the alignments themselves (in GenomeThreader format), alignment structures suitable for genome annotation workflows (in GFF3 format), and documentation providing complete disclosure of the alignment procedure.

## Synopsis

Reference protein sequences from Apis mellifera ([OGS 3.2][] & [NCBI GNOMON][]) and Drosophila melanogaster ([FlyBase r5.55][]) were splice-aligned to the genome using [GenomeThreader][] version 1.6.0.

## Data access

The repeat-masked *P. dominula* reference genome assembly is available for download at the DOI [10.6084/m9.figshare.1593187][maskgenomedoi].
Proteins from the *Apis mellifera* Official Gene Set (OGS) 3.2 are available from HymenopteraBase, and proteins from NCBI's annotation of *A. mellifera* are available from GenBank.
Proteins from the *Drosophila melanogaster* annotation release 5.55 are available at FlyBase.

The protein sequences were downloaded using the following commands.

```bash
BeeData=http://hymenopteragenome.org/beebase/sites/hymenopteragenome.org.beebase
curl ${BeeData}/files/data/consortium_data/amel_OGSv3.2_pep.fa.gz \
    | zcat \
    | sed 's/gnl|Amel_4.5|//g' \
    > amel-ogs-prot.fa
curl ftp://ftp.ncbi.nih.gov/genomes/Apis_mellifera/protein/protein.fa.gz \
    | zcat \
    | perl -ne 's/>gi\|(\d+)\|ref\|([^|]+)\|\S*/>$1 $2/; print' \
    > amel-ncbi-prot.fa
FlyData=ftp://ftp.flybase.net/releases/FB2014_01/dmel_r5.55
curl ${FlyData}/fasta/dmel-all-translation-r5.55.fasta.gz \
    | zcat \
    > dmel-flybase-prot.fa
```

## Procedure

First, we set environmental variables necessary for GenomeThreader to function properly.

```bash
export GTHBIN=/usr/local/src/gth/bin
export PATH=$GTHBIN:$PATH
export BSSMDIR=$GTHBIN/bssm
export GTHDATADIR=$GTHBIN/gthdata
```

The proteins were then aligned using the following commands.

```bash
for prot in amel-ogs amel-ncbi dmel-flybase
do
  gth -genomic pdom-scaffolds-masked-r1.2.fa \
      -protein ${prot}-prot.fa \
      -species arabidopsis \
      -gcmaxgapwidth 20000 \
      -gcmincoverage 25 \
      -prhdist 6 \
      -prminmatchlen 18 \
      -prseedlength 6 \
      -o ${prot}-prot-masked.gth \
      -force \
      > ${prot}-prot-masked.log 2>&1
done
```

Finally, the GenomeThreader alignments were converted to GFF3 format, filtering out alignments with similarity or coverage scores < 0.5.

```bash
for prot in amel-ogs amel-ncbi dmel-flybase
do
  ./gth2makergff3.py < ${prot}-prot-masked.gth > ${prot}-prot-masked.gff3
done
```

------

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)][ccby4]  
This work is licensed under a [Creative Commons Attribution 4.0 International License][ccby4].


[pdomproj]: https://github.com/PdomGenomeProject
[maskgenomedoi]: http://dx.doi.org/10.6084/m9.figshare.1593187
[OGS 3.2]: http://hymenopteragenome.org/beebase/?q=download_sequences
[NCBI GNOMON]: ftp://ftp.ncbi.nih.gov/genomes/Apis_mellifera/protein
[FlyBase r5.55]: ftp://ftp.flybase.net/releases/FB2014_01/dmel_r5.55
[GenomeThreader]: http://genomethreader.org
[ccby4]: http://creativecommons.org/licenses/by/4.0/
