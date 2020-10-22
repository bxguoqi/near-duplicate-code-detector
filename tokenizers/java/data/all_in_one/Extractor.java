package javatokenizer;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.DirectoryFileFilter;
import org.apache.commons.io.filefilter.TrueFileFilter;

import java.io.FileOutputStream;
import java.io.FilenameFilter;
import java.io.File;
import java.io.OutputStreamWriter;
import java.io.IOException;
import java.io.Writer;
import java.nio.charset.Charset;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Spliterators;
import java.util.stream.StreamSupport;
import java.util.zip.GZIPOutputStream;

import com.github.javaparser.JavaParser;
import com.github.javaparser.JavaToken;
import com.github.javaparser.ast.CompilationUnit;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;


public class Extractor {

    public static void main(String[] args) throws IOException {
        if (args.length != 3) {
            System.err.println("Usage <projectsFolder> <outputFolder> true|false");
            System.exit(-1);
        }

        File projectFolder = new File(args[0]);
        File outputFolder = new File(args[1]);

        String[] projectFolders = projectFolder.list(new FilenameFilter() {
            @Override
            public boolean accept(File current, String name) {
              return new File(current, name).isDirectory();
            }
          });
          Arrays.stream(projectFolders).forEach(f->ExtractForFolder(new File(projectFolder, f),
                outputFolder, Boolean.parseBoolean(args[2]), projectFolder));
    }

    public static void ExtractForFolder(File projectFolder, File outputFolder, boolean onlyIdentifiers, File baseFolder) {
        Iterator<File> allFiles = FileUtils.iterateFiles(projectFolder, new String[] {"java"}, true);
        try {
            FileOutputStream output = new FileOutputStream(Paths.get(outputFolder.toPath().toString(),  projectFolder.getName() + ".jsonl.gz").toFile());
            Gson gson = new GsonBuilder().create();

            try {
                Writer writer = new OutputStreamWriter(new GZIPOutputStream(output), "UTF-8");
                Iterable<File> fileIter = ()-> allFiles;
                StreamSupport.stream(
                    fileIter.spliterator(), true).map(f-> TokenizeFile(f, onlyIdentifiers, baseFolder))
                    .map(t->gson.toJson(t)).filter(g->g!=null).sequential().forEach(g->{
                        try{
                            writer.write(g);
                            writer.write('\n');
                        } catch (IOException ioe) {
                            // really?
                            ioe.printStackTrace();
                        }
                    });
                writer.close();
            } catch(Exception e) {
                System.out.println("Error for project " + projectFolder + ": " + e);
                e.printStackTrace();
            } finally {
                output.close();
            }
        } catch (IOException e) {
            System.out.println("Error for project " + projectFolder + ": " + e);
            e.printStackTrace();
        }
    }
    public static void ExtractForFolder2(File projectFolder, File outputFolder, boolean onlyIdentifiers, File baseFolder) {
        Iterator<File> allFiles = FileUtils.iterateFiles(projectFolder, new String[] {"java"}, true);
        try {
            FileOutputStream output = new FileOutputStream(Paths.get(outputFolder.toPath().toString(),  projectFolder.getName() + ".jsonl.gz").toFile());
            Gson gson = new GsonBuilder().create();

            try {
                Writer writer = new OutputStreamWriter(new GZIPOutputStream(output), "UTF-8");
                Iterable<File> fileIter = ()-> allFiles;
                StreamSupport.stream(
                        fileIter.spliterator(), true).map(f-> TokenizeFile(f, onlyIdentifiers, baseFolder))
                        .map(t->gson.toJson(t)).filter(g->g!=null).sequential().forEach(g->{
                    try{
                        writer.write(g);
                        writer.write('\n');
                    } catch (IOException ioe) {
                        // really?
                        ioe.printStackTrace();
                    }
                });
                writer.close();
            } catch(Exception e) {
                System.out.println("Error for project " + projectFolder + ": " + e);
                e.printStackTrace();
            } finally {
                output.close();
            }
        } catch (IOException e) {
            System.out.println("Error for project " + projectFolder + ": " + e);
            e.printStackTrace();
        }
    }
}
